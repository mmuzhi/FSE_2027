from __future__ import annotations

import json
import argparse
from pathlib import Path

TASK_FILES = {
    'generation': 'generation_judge_results.jsonl',
    'execution': 'execution_judge_results.jsonl',
    'debug': 'debug_judge_results.jsonl',
    'translation': 'translation_judge_results.jsonl',
}


def load_judge_results(file_path: Path) -> dict[str, dict]:
    results = {}
    if not file_path.exists():
        return results
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                task_id = data.get('task_id')
                if task_id:
                    results[task_id] = data
            except json.JSONDecodeError:
                continue
    return results


def aggregate_all_samples(
    all_results: dict[str, dict[str, dict]],
    method: str = 'weighted_vote'
) -> dict[str, dict]:
    all_task_ids = set().union(*(llm_results.keys() for llm_results in all_results.values()))
    aggregated = {}
    
    for task_id in all_task_ids:
        all_samples = []
        llm_summaries = {}
        
        for llm_name, llm_results in all_results.items():
            if task_id not in llm_results:
                continue
            
            result = llm_results[task_id]
            samples = result.get('samples', [])
            
            llm_valid_count = 0
            llm_invalid_count = 0
            llm_confidences = []
            
            for sample in samples:
                label = sample.get('label', 'Invalid')
                confidence = sample.get('confidence', 0.5)
                sample_idx = sample.get('sample_idx', 0)
                
                all_samples.append({
                    'llm': llm_name,
                    'sample_idx': sample_idx,
                    'label': label,
                    'confidence': confidence,
                })
                
                if label == 'Valid':
                    llm_valid_count += 1
                else:
                    llm_invalid_count += 1
                llm_confidences.append(confidence)
            
            if samples:
                llm_summaries[llm_name] = {
                    'valid_count': llm_valid_count,
                    'invalid_count': llm_invalid_count,
                    'total_samples': len(samples),
                    'avg_confidence': sum(llm_confidences) / len(llm_confidences),
                    'final_label': result.get('final_label', 'Unknown'),
                }
        
        if not all_samples:
            continue
        
        total_samples = len(all_samples)
        valid_samples = [s for s in all_samples if s['label'] == 'Valid']
        invalid_samples = [s for s in all_samples if s['label'] == 'Invalid']
        
        valid_count = len(valid_samples)
        invalid_count = len(invalid_samples)
        
        if method == 'majority_vote':
            final_label = 'Valid' if valid_count > invalid_count else 'Invalid'
            if valid_count == invalid_count:
                valid_conf = sum(s['confidence'] for s in valid_samples) / valid_count if valid_count > 0 else 0
                invalid_conf = sum(s['confidence'] for s in invalid_samples) / invalid_count if invalid_count > 0 else 0
                final_label = 'Valid' if valid_conf >= invalid_conf else 'Invalid'
            
            winner_count = valid_count if final_label == 'Valid' else invalid_count
            final_confidence = winner_count / total_samples
            
        elif method == 'weighted_vote':
            valid_score = sum(s['confidence'] for s in valid_samples)
            invalid_score = sum(s['confidence'] for s in invalid_samples)
            
            total_score = valid_score + invalid_score
            if total_score > 0:
                final_label = 'Valid' if valid_score > invalid_score else 'Invalid'
                winner_score = valid_score if final_label == 'Valid' else invalid_score
                final_confidence = winner_score / total_score
            else:
                final_label = 'Invalid'
                final_confidence = 0.5
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        llm_names = list(llm_summaries.keys())
        llm_agreement = sum(1 for llm in llm_names 
                           if llm_summaries[llm]['final_label'] == final_label)
        
        aggregated[task_id] = {
            'task_id': task_id,
            'final_label': final_label,
            'is_valid': final_label == 'Valid',
            'confidence': round(final_confidence, 4),
            'valid_votes': valid_count,
            'invalid_votes': invalid_count,
            'total_votes': total_samples,
            'vote_ratio': f"{valid_count}/{total_samples}",
            'valid_ratio': round(valid_count / total_samples, 4) if total_samples > 0 else 0,
            'num_llms': len(llm_summaries),
            'llm_agreement': f"{llm_agreement}/{len(llm_names)}",
            'llm_details': llm_summaries,
            'all_samples': all_samples,
        }
    
    return aggregated


def process_single_task(
    results_dir: Path,
    task_name: str,
    file_pattern: str,
    method: str
) -> dict | None:
    llm_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
    all_results = {}
    llm_stats = {}
    
    for llm_dir in llm_dirs:
        result_file = llm_dir / file_pattern
        if result_file.exists():
            results = load_judge_results(result_file)
            if results:
                all_results[llm_dir.name] = results
                llm_stats[llm_dir.name] = len(results)
    
    if not all_results:
        return None
    
    aggregated = aggregate_all_samples(all_results, method=method)
    
    if not aggregated:
        return None
    
    valid_count = sum(1 for r in aggregated.values() if r['is_valid'])
    invalid_count = len(aggregated) - valid_count
    
    unanimous_valid = sum(1 for r in aggregated.values() 
                          if r['valid_votes'] == r['total_votes'])
    unanimous_invalid = sum(1 for r in aggregated.values() 
                            if r['invalid_votes'] == r['total_votes'])
    disagreed = len(aggregated) - unanimous_valid - unanimous_invalid
    
    avg_confidence = sum(r['confidence'] for r in aggregated.values()) / len(aggregated)
    
    return {
        'task_name': task_name,
        'llm_stats': llm_stats,
        'total_tasks': len(aggregated),
        'valid_count': valid_count,
        'invalid_count': invalid_count,
        'unanimous_valid': unanimous_valid,
        'unanimous_invalid': unanimous_invalid,
        'disagreed': disagreed,
        'avg_confidence': avg_confidence,
        'results': aggregated,
    }


def main():
    repo_root = Path(__file__).resolve().parents[1]
    
    parser = argparse.ArgumentParser(description="Aggregate Judge Results from Multiple LLMs")
    parser.add_argument('--cot_model', type=str, default='qwen',
                        help="CoT model to aggregate (e.g., 'r1', 'qwen')")
    parser.add_argument('--task', type=str, default=None,
                        help="Specific task to process (default: all tasks)")
    parser.add_argument('--method', type=str, default='weighted_vote',
                        choices=['majority_vote', 'weighted_vote'],
                        help="Aggregation method")
    parser.add_argument('--verbose', action='store_true',
                        help="Print detailed results")
    
    args = parser.parse_args()
    
    results_dir = repo_root / 'data' / 'derived_cot' / 'rq2_judging' / args.cot_model
    if not results_dir.exists():
        print(f"Error: Directory not found: {results_dir}")
        return
    
    llm_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
    if not llm_dirs:
        print(f"Error: No LLM directories found in {results_dir}")
        return
    
    print(f"Found {len(llm_dirs)} LLM(s): {[d.name for d in llm_dirs]}")
    print(f"Aggregation method: {args.method}")
    print("=" * 60)
    
    if args.task:
        if args.task not in TASK_FILES:
            print(f"Error: Unknown task '{args.task}'. Available: {list(TASK_FILES)}")
            return
        task_files = {args.task: TASK_FILES[args.task]}
    else:
        task_files = TASK_FILES
    
    all_task_results = {}
    
    for task_name, file_pattern in task_files.items():
        print(f"\n[{task_name.upper()}]")
        
        result = process_single_task(
            results_dir=results_dir,
            task_name=task_name,
            file_pattern=file_pattern,
            method=args.method
        )
        
        if result is None:
            print(f"  No results found for {task_name}")
            continue
        
        all_task_results[task_name] = result
        
        print(f"  LLMs: {result['llm_stats']}")
        print(f"  Total tasks: {result['total_tasks']}")
        print(f"  Valid: {result['valid_count']} ({100*result['valid_count']/result['total_tasks']:.1f}%)")
        print(f"  Invalid: {result['invalid_count']} ({100*result['invalid_count']/result['total_tasks']:.1f}%)")
        print(f"  Unanimous Valid: {result['unanimous_valid']}, Unanimous Invalid: {result['unanimous_invalid']}, Disagreed: {result['disagreed']}")
        print(f"  Average Confidence: {result['avg_confidence']:.3f}")
        
        if args.verbose:
            print(f"\n  Detailed Results:")
            for task_id, r in sorted(result['results'].items()):
                label = "✓ Valid" if r['is_valid'] else "✗ Invalid"
                print(f"    {task_id}: {label} (conf={r['confidence']:.2f}, votes={r['vote_ratio']}, llm_agree={r['llm_agreement']})")
                for llm_name, llm_info in r['llm_details'].items():
                    print(f"      - {llm_name}: {llm_info['final_label']} (v={llm_info['valid_count']}, i={llm_info['invalid_count']}, conf={llm_info['avg_confidence']:.2f})")
    
    if not all_task_results:
        print("\nNo results found for any task")
        return
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_valid = sum(r['valid_count'] for r in all_task_results.values())
    total_invalid = sum(r['invalid_count'] for r in all_task_results.values())
    total_tasks = total_valid + total_invalid
    
    print(f"Total across all tasks: {total_tasks}")
    print(f"  Valid: {total_valid} ({100*total_valid/total_tasks:.1f}%)")
    print(f"  Invalid: {total_invalid} ({100*total_invalid/total_tasks:.1f}%)")
    
    saved_files = []
    
    for task_name, task_result in all_task_results.items():
        output_path = results_dir / f"aggregated_{task_name}.json"
        
        output_data = {
            'meta': {
                'cot_model': args.cot_model,
                'task': task_name,
                'method': args.method,
                'llms': [d.name for d in llm_dirs],
                'llm_stats': task_result['llm_stats'],
                'total_tasks': task_result['total_tasks'],
                'valid_count': task_result['valid_count'],
                'invalid_count': task_result['invalid_count'],
                'unanimous_valid': task_result['unanimous_valid'],
                'unanimous_invalid': task_result['unanimous_invalid'],
                'disagreed': task_result['disagreed'],
                'avg_confidence': task_result['avg_confidence'],
            },
            'results': list(task_result['results'].values())
        }
        
        output_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
        
        saved_files.append(output_path)
    
    print(f"\nSaved {len(saved_files)} files:")
    for f in saved_files:
        print(f"  - {f}")


if __name__ == '__main__':
    main()
