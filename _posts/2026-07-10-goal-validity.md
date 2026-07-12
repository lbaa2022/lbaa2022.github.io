---
layout: post
title: 2026년의 AI는 아직 "모른다"고 말하지 못합니다 — LBA 연구가 계속 유효한 이유
tags: [연구동향,벤치마크,불확실성]
categories: Demo
author: thibault
date: 2026-07-10
---

지난 몇 년 사이 인공지능은 눈부시게 발전했습니다. 최신 대규모 언어모델(Large Language Model, LLM)은 수학 올림피아드 문제를 풀고, 긴 코드를 작성하며, 사람과 자연스럽게 대화합니다. 그렇다면 "모르는 것을 자각하고, 물어서 배우는 로봇 지능"을 목표로 2022년에 출발한 본 과제(LBA: Learning By Asking)의 문제는 이미 풀린 것일까요? 최근 공개된 벤치마크(benchmark) 결과들은 그렇지 않다고 답합니다.

**첫째, 최신 모델도 모르는 것을 모른다고 판정하지 못합니다.** OpenAI가 2025년 8월 공개한 GPT-5의 시스템 카드에 따르면, 단답형 사실 질문 평가 SimpleQA에서 gpt-5-main의 환각(hallucination) 비율은 47%에 이릅니다[1]. 더 흥미로운 사실도 있습니다. 추론 특화 모델 o3는 인물 사실성 평가 PersonQA에서 환각 비율 33%를 기록해 전 세대 o1(16%)의 두 배에 달했고, OpenAI 스스로 "원인을 이해하려면 더 많은 연구가 필요하다"고 적었습니다[2]. 추론 성능의 향상이 불확실성 자각을 자동으로 개선해 주지 않는다는 뜻입니다.

**둘째, 모를 때 무엇을 물어야 하는지 알지 못합니다.** Google DeepMind의 QuestBench는 정보가 하나 빠진 문제에서 LLM이 올바른 질문을 찾아내는 능력을 재는데, 최신 모델들이 수학 문제에서는 잘하지만 논리·계획 문제에서는 정확도가 40~50%에 머물렀습니다[3]. 로봇의 작업 계획과 같은 꼴의 문제에서 질문 능력이 가장 약하다는 결과입니다. Meta의 AbstentionBench는 프런티어 모델 20종을 20개 데이터셋에서 평가해, 답할 수 없는 질문 앞에서 응답을 유보(abstention)하는 능력은 모델 규모를 키워도 거의 나아지지 않으며, 추론 파인튜닝은 오히려 유보 능력을 평균 24% 떨어뜨린다고 보고했습니다[4].

**셋째, 새로 배우면 이전 것을 잊습니다.** 파국적 망각(catastrophic forgetting)은 파운데이션 모델 시대에도 해소되지 않았습니다. 1B~7B 규모 LLM의 지속 파인튜닝에서 망각이 일반적으로 관찰되고 모델 규모가 커질수록 오히려 심해진다는 실증 결과가 보고되었으며[5], 파운데이션 모델 기반 지속 학습은 서베이 문헌에서도 여전히 열린 문제로 정리되고 있습니다[6].

**넷째, 절차 추론의 신뢰도는 실용 수준에 미치지 못합니다.** 본 과제가 개발해 ICLR 2024에 발표한 LoTa-Bench는 언어 기반 작업 계획기(task planner)의 성능을 자동으로 재는 벤치마크로, ALFRED 환경에서 GPT-3(text-davinci-003)의 성공률 21.36%, GPT-4의 성공률 40.38%를 측정해 이 문제의 난도를 정량적으로 보여 주었습니다[7]. 후속 국제 벤치마크들의 결과도 같은 방향입니다. 2025년 발표된 EmbodiedBench에서는 멀티모달 모델 24종 가운데 최고인 GPT-4o가 1,128개 과업에서 평균 성공률 28.9%에 그쳤고[8], NeurIPS 2024의 Embodied Agent Interface에서는 최상위 모델 o1-preview조차 BEHAVIOR 시뮬레이터의 부분목표 분해에서 성공률 57.0%였으며, 목표가 10개를 넘는 과업은 성공률이 40% 아래로 떨어졌습니다[9]. 이 난제를 재는 도구를 본 과제의 산출물로 국제 학계에 먼저 내놓았다는 사실은 저희에게 작지 않은 자부심입니다.

정리하면 이렇습니다. 모르는 것을 자각하는 능력, 모를 때 묻는 능력, 잊지 않고 계속 배우는 능력, 신뢰할 수 있는 절차 추론 — 이 네 가지는 2026년 현재에도 최신 AI가 갖추지 못한 능력입니다. AI가 로봇이라는 물리적 실체에 실려 사람 곁에서 움직일수록, "모른다"고 말하고 물어서 배우는 능력은 안전과 신뢰의 전제 조건이 됩니다. LBA 과제가 겨냥한 문제는 아직 살아 있고, 그래서 지금 더 중요해졌습니다.

*작성: Thibault · 요청: 장민수(ETRI)*

## 출처

1. OpenAI, GPT-5 System Card (2025-08), Table 8: SimpleQA (no web), gpt-5-main hallucination rate 0.47. [https://cdn.openai.com/gpt-5-system-card.pdf](https://cdn.openai.com/gpt-5-system-card.pdf)
2. OpenAI, OpenAI o3 and o4-mini System Card (2025-04), Table 4: PersonQA hallucination rate o3 0.33 vs o1 0.16. [https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf)
3. Li, B. Z., Kim, B., and Wang, Z. (Google DeepMind), "QuestBench: Can LLMs ask the right question to acquire information in reasoning tasks?" (2025). [https://arxiv.org/abs/2503.22674](https://arxiv.org/abs/2503.22674)
4. Kirichenko, P., Ibrahim, M., Chaudhuri, K., and Bell, S. J. (Meta AI), "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions" (2025). [https://arxiv.org/abs/2506.09038](https://arxiv.org/abs/2506.09038)
5. Luo, Y. et al., "An Empirical Study of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning" (2023). [https://arxiv.org/abs/2308.08747](https://arxiv.org/abs/2308.08747)
6. Yang, Y. et al., "Recent Advances of Foundation Language Models-based Continual Learning: A Survey", ACM Computing Surveys (2024). [https://dl.acm.org/doi/10.1145/3705725](https://dl.acm.org/doi/10.1145/3705725)
7. Choi, J.-W., Yoon, Y., Ong, H., Kim, J., and Jang, M. (ETRI), "LoTa-Bench: Benchmarking Language-oriented Task Planners for Embodied Agents", ICLR 2024. [https://arxiv.org/abs/2402.08178](https://arxiv.org/abs/2402.08178)
8. Yang, R. et al., "EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents" (2025). [https://arxiv.org/abs/2502.09560](https://arxiv.org/abs/2502.09560)
9. Li, M. et al. (Stanford), "Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making", NeurIPS 2024 Datasets and Benchmarks. [https://arxiv.org/abs/2410.07166](https://arxiv.org/abs/2410.07166)
