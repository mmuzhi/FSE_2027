ICSE 2027 Paper #135 Reviews and Comments.txt
ICSE 2027 Paper #135 Reviews and Comments
===========================================================================
Paper #135 Reasoning Patterns for Efficient AI Coding: An Empirical Study


Review #135A
===========================================================================

Overall merit
-------------
2. Weak reject

Novelty
-------
2. Incremental - modest extension, adaptation, combination, or improvement

Rigor
-----
2. Fair - some weaknesses, but the main claims are at least partially
   supported

Relevance
---------
2. Moderate - relevant and useful, but the expected impact is limited or
   narrowly scoped

Verifiability and Transparency
------------------------------
1. Weak - Key information is missing; the work or main claims are difficult
   to verify

Presentation
------------
2. Fair - understandable, but with noticeable clarity or organization
   issues

Paper summary
-------------
The paper analyzes how reasoning models think during coding tasks by mapping their reasoning traces onto a taxonomy of eight actions and mining frequent patterns across four tasks and two DeepSeek-R1 models. The main findings are that each task has its own characteristic reasoning structure and that trace validity is marked by verification-driven convergence rather than repeated design revision and reflection.

Strengths
---------
- The paper addresses a timely and relevant topic by understanding how reasoning models behave in coding tasks and studying them at a reasonable scale across four different tasks.
- The idea of treating reasoning traces as structured behavioral data rather than plain text is interesting and worth exploring.

Weaknesses
----------
- Unjustified model choices, the two subject models are a teacher and its own distillation, so cross-model consistency is expected.
- The RQ2 validity construct risks circularity, labels and features both come from LLMs reading the same text, with no check against the correctness oracle.
- Missing methodological detail prevents reproduction.

Detailed comments for authors
-----------------------------
### Novelty

The novelty of the paper is overall moderate. The core components for code generation already exist (and are also presented in the related work section): [7] builds a finer 15-action taxonomy through human open coding, correlates actions with pass@1, and tests findings-informed prompting, while [20] contrasts successful and failed traces and shows, via step-budget cuts, that chains carry 10 to 30% removable content. 

The genuine increments here are the cross-task scope, the ordered transition-level representation of patterns, and the online anti-pattern early stopping. The taxonomy, the behavior-correctness contrast, and pattern-guided prompting are incremental. Given this, the "first empirical study" claim rests entirely on the cross-task qualifier and should be softened.

### Rigor

I have several issues with the rigor of the paper, and a large share of them stem from a lack of specifications and motivation for the use of specific models.

First of all, we have the models that serve as the core of the study: DeepSeek-R1-0528 and DeepSeek-R1-0528-Qwen-8B. Why these two models were chosen, and how they can be used to generalize the findings to all models that produce reasoning, are never explained or justified. Note also that, as written in the paper, the second is a distillation of the first, so the reported cross-model consistency is largely expected.

Then, please consider that DeepSeek-R1-0528 is a 685B-parameter model, and its reasoning traces and performance are being compared with those of an 8B model. This aspect needs to be better justified, and how potential issues that could arise from the difference in parameter size were mitigated

How the models used in the LLM-as-a-judge setting were selected, on what criteria, and how they were used are never explained. Most critically, the paper later says that two other models were used to annotate the reasoning traces, another thing that is never motivated.

Finally, the sampling temperature and top-p are given, but there is no indication of how the models used in the study were invoked (API? Self-hosted?), and the checkpoints for the open models that were used (key points for reproducibility, see below). 

Beyond the issues of model selection, I think that the central RQ2 construct is at risk of circularity. Section II-B2 defines invalid traces as logical inconsistencies or unnecessary reasoning detours, and Finding 2 reports that invalid traces exhibit repeated design revisions, reflections, and knowledge recall without progressing toward closure, with several anti-patterns literally named detours in Table IV. Since both the labels and the action features come from LLMs reading the same trace text with no external anchor, the reported enrichment is compatible with the labels having been assigned partly on the basis of those very patterns. The paper provides no evidence to rule this out, the judge instructions, per-judge agreement, and the relation between validity labels and the correctness oracle are all missing. A simple check would be to repeat the RQ2 contrast with groups defined by the oracle (pass versus fail) and report whether the anti-patterns remain enriched.

The results for RQ3 lack the necessary controls to attribute the gains to the mined patterns. For prompting, Section V-B describes only a default and a pattern-guided arm, and the authors themselves state that controlled ablations are still needed to isolate pattern-specific guidance from generic instruction effects. Please add such a control, for example, identical generic advice across tasks and a mismatched arm applying one task's patterns to another.

The mining thresholds (0.05/0.03 and 0.08/0.06) are handpicked without any sensitivity analysis.

Minor:

Given that the action taxonomy is derived by prior works, it could be useful to also have an indication of the source of each action.

### Relevance

Given that the paper frames its results to be beneficial to AI coding in general, but has tested on two models (with all the issues identified above). Moreover, since all four benchmarks are small algorithmic or class-level tasks, the implications for realistic software engineering practice (repo-level or agentic settings) remain untested.

### Verifiability and Transparency

The paper provides a replication package with prompts, enabling verification of the results. 

However, there are issues in the paper that prevent the study from being reproduced. The size of the re-annotated subset behind the kappa is unspecified; the procedure for combining the two annotator models is not described; per-judge agreement and the number of human-adjudicated validity cases are missing; checkpoints and serving details are absent. For early stopping, the paper never states which model performs the online mapping of streaming text to actions or what it costs, so the reported 30 to 69% savings cannot be verified end-to-end.

### Presentation

The paper is generally well written, and the English is good. However, some parts have a high density of figures and tables (pages 4 to 6 pack Tables III to V plus Figures 2 and 3 into a short span), and Section II contains a high density of math formulas for what are simple concepts (proportions, transition frequencies, weighted voting), which makes the reading a little less easy. Consider moving some notation to a table or simplifying it to text-only.

Minor Comments:

The tables are inconsistent in styling, please make them uniform.

Questions for authors’ response
-------------------------------
Why were DeepSeek-R1-0528 and its 8B distillation chosen as the subject models, and how can findings from a model and its own distillation support claims of cross-model generality?



Review #135B
===========================================================================

Overall merit
-------------
2. Weak reject

Novelty
-------
2. Incremental - modest extension, adaptation, combination, or improvement

Rigor
-----
2. Fair - some weaknesses, but the main claims are at least partially
   supported

Relevance
---------
3. High - addresses an important SE problem and is likely to influence
   research or practice under clear assumptions

Verifiability and Transparency
------------------------------
3. Good - Sufficient information is provided to understand the work and
   support verification of the main claims

Presentation
------------
2. Fair - understandable, but with noticeable clarity or organization
   issues

Paper summary
-------------
The paper presents an empirical study of reasoning patterns in LRM-based AI coding. It abstracts reasoning traces into sequences over an action taxonomy, then mines macro patterns (task-level reasoning strategies) and micro patterns (fine-grained behaviors distinguishing valid from invalid traces, including anti-patterns). The study spans four coding tasks and two DeepSeek-R1-family models, and demonstrates three applications: task classification, pattern-guided prompting, and pattern-aware early stopping.

Strengths
---------
- The high-level framing (turning free-form traces into action sequences) is intuitive and readable.
- The study covers four coding tasks rather than a single task.
- It combines automatic annotation with human validation and statistical testing.
- The finding that invalid traces are longer, not shorter, is genuinely counterintuitive and interesting.

Weaknesses
----------
- Limited novelty; largely a multi-task extension of prior single-task work plus a few applications.
- Core definitions are circular or opportunistic, and thresholds are hand-tuned with no sensitivity analysis.
- The early-stopping application is not realizable as described, and its cost is not accounted for. Validity labeling relies on LLM judges with insufficient human verification.

Detailed comments for authors
-----------------------------
The paper studies reasoning patterns in LRM-based AI coding by abstracting reasoning traces into action sequences over an eight-action taxonomy, mining macro patterns (task-level strategies) and micro patterns (valid vs. invalid behaviors), and demonstrating three applications across four coding tasks and two models. The finding that invalid traces are longer, not shorter, is genuinely counterintuitive and interesting. I am curious that does longer traces necessarily lead to more tokens? 

However, the work is thin on novelty and research challenge. The cited related work studies reasoning behaviors mostly on single tasks. The closest being [7] on code generation and [36] on code execution. This paper's contribution is therefore primarily the multi-task extension plus applications, yet the RQs do not exploit the multi-task design. 

The early-stopping application (RQ3.3) is somewhat weak. Detecting anti-patterns requires an action-labeled trace, but the paper's action labeling is done offline by several large LLMs on complete traces; how the same labels are produced online, on partial prefixes, during generation is never specified. If an LLM tags each segment, that monitoring cost is not counted against the reported 30–69% savings; if a lighter mechanism is used, its labels may diverge from the offline labels the anti-patterns were mined from. As written, this experiment is not reproducible and the savings claim is not fully supported.

Finally, the evidence for the applications and for generality is limited. Pattern-guided prompting yields small and inconsistent gains (with some regressions) and, as the authors admit, lacks the ablation needed to separate pattern-specific guidance from generic instruction effects. The "cross-model" and "transfer" claims also overstate independence, as the two core models share the same lineage (one is a distillation of the other), and one transfer model is also DeepSeek family, leaving GLM-5.1 as the only truly independent model. 

Presentation:
- Sections II-C and II-D are hard to follow; a single end-to-end worked example would greatly improve clarity.
- Action labels are reused with conflicting meanings (SD: "Solution design" → "design reopening"; AUX: "Auxiliary" → "answer finalization"). Terminology should be consistent.
- Key constructs such as "closure share" and "drift share" are introduced abstractly and need clearer, up-front definitions.
- In section II, for the two parts using ensemble LLM as a judge, please share the prompt.

Artifact assessment
-------------------
3. Satisfactory, i.e., the artifacts are in line with what is declared in
   the submission form or the paper [OR] the authors explained why the
   artifacts are not provided and I find the explanation to be reasonable.

Comments on artifact assessment
-------------------------------
The anonymized repository is available and populated, and its README is well-organized around RQ1–RQ3 with scripts, the four declared benchmarks, pre-computed outputs, and the annotation and judge prompts that the paper omits. The declared contents are consistent with the paper.

Questions for authors’ response
-------------------------------
1. Does trace validity correlate with task correctness?

2. In Section II. B. (3) when accessoing annotation reliability of LLM judges, the paper only reported the agreement among human annotators. But what about between human and LLM judges?

3. When labeling valid/invalid traces, does valid trace need to have correct answer?



Review #135C
===========================================================================

Overall merit
-------------
2. Weak reject

Novelty
-------
1. Limited - largely known or only minor variation over prior work

Rigor
-----
2. Fair - some weaknesses, but the main claims are at least partially
   supported

Relevance
---------
3. High - addresses an important SE problem and is likely to influence
   research or practice under clear assumptions

Verifiability and Transparency
------------------------------
3. Good - Sufficient information is provided to understand the work and
   support verification of the main claims

Presentation
------------
3. Good - clear, well organized, and easy to follow

Paper summary
-------------
The paper provides set of high and low-level reasoning patterns extracted from LRM's trajectories.  They show that the patterns are different per task.
To show the usefulness of the patterns, they apply them in 3 tasks: Coding Task Classification, Pattern-Guided Prompting,  Pattern-Aware Early Stopping. 
The show that  patterns improves accurate task identification and single-attempt correctness.
Also pattern-aware early stopping reduces cost.

Strengths
---------
- provides a reasoning pattern taxonomy 
- Results are mainly in the right direction

Weaknesses
----------
- Poor evaluation design (choice of tasks)
- insignificant results (transferred)
- over-claim about improvements

Detailed comments for authors
-----------------------------
Although the idea of finding (anti-)patterns of reasoning and using them to improve the process is nice, but the experiments did not deliver the evidence required to accept the hypotheses.
I still appreciate the pattern categories themselves, but the application part is not well-justified. 
 
Firstly, why does Coding Task Classification from patterns matter? What is the use case? Is it a user-facing use case or an agentic/LLM use case? I don't believe this task by itself is realistically practical.

I also have concerns about pattern-aware prompting and stopping. The “direct” results in Table V are less interesting since they somehow leak information (using the same model to create the patterns and then use those to better prompt). Looking at the transferred columns results are less significant, both for the P@1 and tokens usage.

Average P@1 improvements is around ~3% and ~0.5% for DS-V4-F and GLM-5.1, respectively. 
So unlike finding 3.2’s claim I would not say the results “suggesting that reasoning
patterns provide transferable, solution-agnostic guidance for improving coding performance.”

Are the patterns in “Pattern-aware Early Stopping” extracted from the same model? If so a transferability analysis is needed like Table V.

Table VI results are on the edge. Clearly more reasoning and interference time scaling increase the cost to gain accuracy. Whether the extra gains reported (1.21–7.42 percentage-point pass@1) justifies the extra cost is a matter of debate. Often time models are not as trained for conciseness as they are for accuracy, specially smaller models.

Questions for authors’ response
-------------------------------
- Where would the "Coding Task Classification" matter?
- Are the patterns in “Pattern-aware Early Stopping” extracted from the same model?