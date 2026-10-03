import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


TRANSLATION_DIRECTIONS = ('cpp_to_py', 'java_to_py', 'py_to_cpp', 'java_to_cpp')


def normalize_translation_task_id(task_id: str) -> str:
    if not task_id:
        return task_id

    if '/' in task_id:
        direction, rest = task_id.split('/', 1)
        if direction in TRANSLATION_DIRECTIONS:
            return f"{direction}/{rest}"
        return task_id

    for direction in TRANSLATION_DIRECTIONS:
        prefix = f"{direction}_"
        if task_id.startswith(prefix):
            return f"{direction}/{task_id[len(prefix):]}"

    return task_id


def normalize_translation_result_keys(results: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for task_id, payload in results.items():
        normalized_id = normalize_translation_task_id(task_id)
        if isinstance(payload, dict):
            payload = {**payload, 'task_id': normalized_id}
        normalized[normalized_id] = payload
    return normalized


def load_aggregated_results(file_path: Path) -> Dict[str, dict]:
    if not file_path.exists():
        return {}
    data = json.loads(file_path.read_text(encoding="utf-8"))
    results = {}
    for item in data.get('results', []):
        task_id = item.get('task_id')
        if task_id:
            results[task_id] = item
    
    return results


def load_test_results(file_path: Path) -> Dict[str, bool]:
    if not file_path.exists():
        return {}
    data = json.loads(file_path.read_text(encoding="utf-8"))
    
    results = {}
    items = data.get('results', [])
    if isinstance(items, list):
        for item in items:
            task_id = item.get('task_id')
            if task_id is None:
                continue
            
            failed = item.get('failed', 0)
            results[task_id] = (failed == 0)
    
    return results


def get_test_file_info(task: str) -> Tuple[str, str]:
    patterns = {
        'generation': ('generation', 'results.json'),
        'execution': ('execution', 'result.json'),
        'debug': ('debug', 'results.json'),
        'translation': ('translation', 'results.json'),
    }
    return patterns.get(task, (task, 'results.json'))


def compute_confusion_matrix(
    cot_results: Dict[str, dict],
    test_results: Dict[str, bool]
) -> Dict[str, Any]:
    common_ids = set(cot_results.keys()) & set(test_results.keys())
    
    tp, fp, fn, tn = 0, 0, 0, 0
    details = {
        'tp': [],
        'fp': [],
        'fn': [],
        'tn': [],
    }
    
    for task_id in common_ids:
        cot_valid = cot_results[task_id].get('is_valid', False)
        test_pass = test_results[task_id]
        
        detail = {
            'task_id': task_id,
            'cot_valid': cot_valid,
            'test_pass': test_pass,
            'confidence': cot_results[task_id].get('confidence', 0),
            'vote_ratio': cot_results[task_id].get('vote_ratio', ''),
        }
        
        if cot_valid and test_pass:
            tp += 1
            details['tp'].append(detail)
        elif cot_valid and not test_pass:
            fp += 1
            details['fp'].append(detail)
        elif not cot_valid and test_pass:
            fn += 1
            details['fn'].append(detail)
        else:
            tn += 1
            details['tn'].append(detail)
    
    total = tp + fp + fn + tn
    
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    return {
        'total_matched': total,
        'cot_only': len(cot_results) - len(common_ids),
        'test_only': len(test_results) - len(common_ids),
        'tp': tp,
        'fp': fp,
        'fn': fn,
        'tn': tn,  # Invalid COT, Fail Test
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'specificity': specificity,
        'details': details,
    }


def analyze_single_task(
    derived_root: Path,
    cot_model: str,
    task: str,
    verbose: bool
) -> Optional[Dict[str, Any]]:
    cot_file = derived_root / 'rq2_judging' / cot_model / f'aggregated_{task}.json'
    cot_results = load_aggregated_results(cot_file)
    
    if not cot_results:
        print(f"  No COT results found: {cot_file}")
        return None
    
    test_subdir, test_filename = get_test_file_info(task)
    test_file = derived_root / 'rq2_eval' / test_subdir / cot_model / test_filename
    test_results = load_test_results(test_file)

    if task.startswith('translation'):
        cot_results = normalize_translation_result_keys(cot_results)
        test_results = normalize_translation_result_keys(test_results)

    if not test_results:
        print(f"  No test results found: {test_file}")
        print(f"  (This task will be skipped, you can add test results later)")
        return None
    
    matrix = compute_confusion_matrix(cot_results, test_results)
    
    print(f"  COT results: {len(cot_results)}, Test results: {len(test_results)}")
    print(f"  Matched tasks: {matrix['total_matched']}")
    if matrix['cot_only'] > 0:
        print(f"  COT only (no test): {matrix['cot_only']}")
    if matrix['test_only'] > 0:
        print(f"  Test only (no COT): {matrix['test_only']}")
    
    print(f"\n  Confusion Matrix:")
    print(f"                    | Test PASS | Test FAIL |")
    print(f"  ------------------|-----------|-----------|")
    print(f"  COT Valid   (预测对) |   TP={matrix['tp']:4d}  |   FP={matrix['fp']:4d}  |")
    print(f"  COT Invalid (预测错) |   FN={matrix['fn']:4d}  |   TN={matrix['tn']:4d}  |")
    
    print(f"\n  Metrics:")
    print(f"    Accuracy:    {matrix['accuracy']:.4f} ({matrix['accuracy']*100:.1f}%)")
    print(f"    Precision:   {matrix['precision']:.4f} (COT说对的里面，实际真对的比例)")
    print(f"    Recall:      {matrix['recall']:.4f} (实际对的里面，COT判对的比例)")
    print(f"    Specificity: {matrix['specificity']:.4f} (实际错的里面，COT判错的比例)")
    print(f"    F1 Score:    {matrix['f1']:.4f}")
    
    if verbose:
        if matrix['fp'] > 0:
            print(f"\n  False Positives (误报: COT说对但测试失败):")
            for d in matrix['details']['fp'][:10]:
                print(f"    - {d['task_id']} (conf={d['confidence']:.2f}, votes={d['vote_ratio']})")
            if len(matrix['details']['fp']) > 10:
                print(f"    ... and {len(matrix['details']['fp']) - 10} more")
        
        if matrix['fn'] > 0:
            print(f"\n  False Negatives (漏报: COT说错但测试通过):")
            for d in matrix['details']['fn'][:10]:
                print(f"    - {d['task_id']} (conf={d['confidence']:.2f}, votes={d['vote_ratio']})")
            if len(matrix['details']['fn']) > 10:
                print(f"    ... and {len(matrix['details']['fn']) - 10} more")
    
    return {
        'task': task,
        'cot_count': len(cot_results),
        'test_count': len(test_results),
        **matrix
    }


def main():
    repo_root = Path(__file__).resolve().parents[1]
    derived_root = repo_root / "data" / "derived_cot"
    
    parser = argparse.ArgumentParser(description="Analyze COT Judge vs Actual Test Results")
    parser.add_argument('--cot_model', type=str, default='r1',
                        help="CoT model to analyze (e.g., 'r1', 'qwen')")
    parser.add_argument('--task', type=str, default=None,
                        help="Specific task to analyze (default: all tasks)")
    parser.add_argument('--verbose', action='store_true',
                        help="Print detailed false positive/negative cases")
    parser.add_argument('--output', type=str, default=None,
                        help="Output file path for analysis results")
    
    args = parser.parse_args()
    
    all_tasks = ['generation', 'execution', 'debug', 'translation']
    
    if args.task:
        if args.task not in all_tasks:
            print(f"Error: Unknown task '{args.task}'. Available: {all_tasks}")
            return
        tasks = [args.task]
    else:
        tasks = all_tasks
    
    print(f"Analyzing COT model: {args.cot_model}")
    print("=" * 60)
    
    all_results = {}
    
    for task in tasks:
        print(f"\n[{task.upper()}]")
        result = analyze_single_task(derived_root, args.cot_model, task, args.verbose)
        if result:
            all_results[task] = result
    
    if not all_results:
        print("\nNo results to analyze")
        return
    
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    
    total_tp = sum(r['tp'] for r in all_results.values())
    total_fp = sum(r['fp'] for r in all_results.values())
    total_fn = sum(r['fn'] for r in all_results.values())
    total_tn = sum(r['tn'] for r in all_results.values())
    total = total_tp + total_fp + total_fn + total_tn
    
    if total > 0:
        overall_accuracy = (total_tp + total_tn) / total
        overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
        overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
        overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0
        
        print(f"Total matched tasks: {total}")
        print(f"  TP: {total_tp}, FP: {total_fp}, FN: {total_fn}, TN: {total_tn}")
        print(f"  Overall Accuracy: {overall_accuracy:.4f} ({overall_accuracy*100:.1f}%)")
        print(f"  Overall Precision: {overall_precision:.4f}")
        print(f"  Overall Recall: {overall_recall:.4f}")
        print(f"  Overall F1: {overall_f1:.4f}")
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = derived_root / 'rq2_judging' / args.cot_model / 'cot_vs_test_analysis.json'
    
    output_data = {
        'meta': {
            'cot_model': args.cot_model,
            'tasks_analyzed': list(all_results.keys()),
        },
        'overall': {
            'total': total,
            'tp': total_tp,
            'fp': total_fp,
            'fn': total_fn,
            'tn': total_tn,
            'accuracy': (total_tp + total_tn) / total if total > 0 else 0,
            'precision': total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0,
            'recall': total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0,
        },
        'tasks': {}
    }
    
    for task, result in all_results.items():
        output_data['tasks'][task] = {k: v for k, v in result.items() if k != 'details'}
        output_data['tasks'][task]['fp_tasks'] = [d['task_id'] for d in result['details']['fp']]
        output_data['tasks'][task]['fn_tasks'] = [d['task_id'] for d in result['details']['fn']]
    
    output_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\nSaved analysis to: {output_path}")


if __name__ == '__main__':
    main()
