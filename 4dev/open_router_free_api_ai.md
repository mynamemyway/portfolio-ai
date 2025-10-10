# Список моделей

## 1. Google: Gemini 2.0 Flash Experimental (free)
- **Размер токенов:** 4,43B tokens
- **Описание:** Gemini Flash 2.0 offers a significantly faster time to first token (TTFT) compared to Gemini Flash 1.5, while maintaining quality on par with larger models like Gemini Pro 1.5. It introduces notable enhancements in multimodal understanding, coding capabilities, complex instruction following, and function calling. These advancements come together to deliver more seamless and robust agentic experiences.
- **Разработчик:** google
- **Контекст:** 1,05M context
- **Цена:** $0/M input tokens, $0/M output tokens

## 2. Qwen: Qwen3 Coder 480B A35B (free)
- **Размер токенов:** 5,32B tokens
- **Описание:** Qwen3-Coder-480B-A35B-Instruct is a Mixture-of-Experts (MoE) code generation model developed by the Qwen team. It is optimized for agentic coding tasks such as function calling, tool use, and long-context reasoning over repositories. The model features 480 billion total parameters, with 35 billion active per forward pass (8 out of 160 experts). Pricing for the Alibaba endpoints varies by context length. Once a request is greater than 128k input tokens, the higher pricing is used.
- **Разработчик:** qwen
- **Контекст:** 262K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 3. TNG: DeepSeek R1T2 Chimera (free)
- **Размер токенов:** 37,5B tokens
- **Описание:** DeepSeek-TNG-R1T2-Chimera is the second-generation Chimera model from TNG Tech. It is a 671 B-parameter mixture-of-experts text-generation model assembled from DeepSeek-AI's R1-0528, R1, and V3-0324 checkpoints with an Assembly-of-Experts merge. The tri-parent design yields strong reasoning performance while running roughly 20 % faster than the original R1 and more than 2× faster than R1-0528 under vLLM, giving a favorable cost-to-intelligence trade-off. The checkpoint supports contexts up to 60 k tokens in standard use (tested to ~130 k) and maintains consistent  token behaviour, making it suitable for long-context analysis, dialogue and other open-ended generation tasks.
- **Разработчик:** tngtech
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 4. DeepSeek: R1 0528 (free)
- **Размер токенов:** 16,5B tokens
- **Описание:** May 28th update to the original DeepSeek R1 Performance on par with OpenAI o1, but open-sourced and with fully open reasoning tokens. It's 671B parameters in size, with 37B active in an inference pass. Fully open-source model.
- **Разработчик:** deepseek
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 5. TNG: DeepSeek R1T Chimera (free)
- **Размер токенов:** 12,9B tokens
- **Описание:** DeepSeek-R1T-Chimera is created by merging DeepSeek-R1 and DeepSeek-V3 (0324), combining the reasoning capabilities of R1 with the token efficiency improvements of V3. It is based on a DeepSeek-MoE Transformer architecture and is optimized for general text generation tasks. The model merges pretrained weights from both source models to balance performance across reasoning, efficiency, and instruction-following tasks. It is released under the MIT license and intended for research and commercial use.
- **Разработчик:** tngtech
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 6. Microsoft: MAI DS R1 (free)
- **Размер токенов:** 6,18B tokens
- **Описание:** MAI-DS-R1 is a post-trained variant of DeepSeek-R1 developed by the Microsoft AI team to improve the model's responsiveness on previously blocked topics while enhancing its safety profile. Built on top of DeepSeek-R1's reasoning foundation, it integrates 110k examples from the Tulu-3 SFT dataset and 350k internally curated multilingual safety-alignment samples. The model retains strong reasoning, coding, and problem-solving capabilities, while unblocking a wide range of prompts previously restricted in R1. MAI-DS-R1 demonstrates improved performance on harm mitigation benchmarks and maintains competitive results across general reasoning tasks. It surpasses R1-1776 in satisfaction metrics for blocked queries and reduces leakage in harmful content categories. The model is based on a transformer MoE architecture and is suitable for general-purpose use cases, excluding high-stakes domains such as legal, medical, or autonomous systems.
- **Разработчик:** microsoft
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 7. DeepSeek: DeepSeek V3 0324 (free)
- **Размер токенов:** 14,5B tokens
- **Описание:** DeepSeek V3, a 685B-parameter, mixture-of-experts model, is the latest iteration of the flagship chat model family from the DeepSeek team. It succeeds the DeepSeek V3 model and performs really well on a variety of tasks.
- **Разработчик:** deepseek
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 8. DeepSeek: R1 (free)
- **Размер токенов:** 6,79B tokens
- **Описание:** DeepSeek R1 is here: Performance on par with OpenAI o1, but open-sourced and with fully open reasoning tokens. It's 671B parameters in size, with 37B active in an inference pass. Fully open-source model & technical report. MIT licensed: Distill & commercialize freely!
- **Разработчик:** deepseek
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 9. DeepSeek: DeepSeek V3.1 (free)
- **Размер токенов:** 227B tokens
- **Описание:** DeepSeek-V3.1 is a large hybrid reasoning model (671B parameters, 37B active) that supports both thinking and non-thinking modes via prompt templates. It extends the DeepSeek-V3 base with a two-phase long-context training process, reaching up to 128K tokens, and uses FP8 microscaling for efficient inference. Users can control the reasoning behaviour with the reasoning enabled boolean. Learn more in our docs The model improves tool use, code generation, and reasoning efficiency, achieving performance comparable to DeepSeek-R1 on difficult benchmarks while responding more quickly. It supports structured tool calling, code agents, and search agents, making it suitable for research, coding, and agentic workflows. It succeeds the DeepSeek V3-0324 model and performs well on a variety of tasks.
- **Разработчик:** deepseek
- **Контекст:** 164K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 10. Tongyi DeepResearch 30B A3B (free)
- **Размер токенов:** 948M tokens
- **Описание:** Tongyi DeepResearch is an agentic large language model developed by Tongyi Lab, with 30 billion total parameters activating only 3 billion per token. It's optimized for long-horizon, deep information-seeking tasks and delivers state-of-the-art performance on benchmarks like Humanity's Last Exam, BrowserComp, BrowserComp-ZH, WebWalkerQA, GAIA, xbench-DeepSearch, and FRAMES. This makes it superior for complex agentic search, reasoning, and multi-step problem-solving compared to prior models. The model includes a fully automated synthetic data pipeline for scalable pre-training, fine-tuning, and reinforcement learning. It uses large-scale continual pre-training on diverse agentic data to boost reasoning and stay fresh. It also features end-to-end on-policy RL with a customized Group Relative Policy Optimization, including token-level gradients and negative sample filtering for stable training. The model supports ReAct for core ability checks and an IterResearch-based 'Heavy' mode for max performance through test-time scaling. It's ideal for advanced research agents, tool use, and heavy inference workflows.
- **Разработчик:** alibaba
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 11. Meituan: LongCat Flash Chat (free)
- **Размер токенов:** 2,9B tokens
- **Описание:** LongCat-Flash-Chat is a large-scale Mixture-of-Experts (MoE) model with 560B total parameters, of which 18.6B–31.3B (≈27B on average) are dynamically activated per input. It introduces a shortcut-connected MoE design to reduce communication overhead and achieve high throughput while maintaining training stability through advanced scaling strategies such as hyperparameter transfer, deterministic computation, and multi-stage optimization. This release, LongCat-Flash-Chat, is a non-thinking foundation model optimized for conversational and agentic tasks. It supports long context windows up to 128K tokens and shows competitive performance across reasoning, coding, instruction following, and domain benchmarks, with particular strengths in tool use and complex multi-step interactions.
- **Разработчик:** meituan
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 12. OpenAI: gpt-oss-20b (free)
- **Размер токенов:** 2,12B tokens
- **Описание:** gpt-oss-20b is an open-weight 21B parameter model released by OpenAI under the Apache 2.0 license. It uses a Mixture-of-Experts (MoE) architecture with 3.6B active parameters per forward pass, optimized for lower-latency inference and deployability on consumer or single-GPU hardware. The model is trained in OpenAI's Harmony response format and supports reasoning level configuration, fine-tuning, and agentic capabilities including function calling, tool use, and structured outputs.
- **Разработчик:** openai
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 13. Z.AI: GLM 4.5 Air (free)
- **Размер токенов:** 27,4B tokens
- **Описание:** GLM-4.5-Air is the lightweight variant of our latest flagship model family, also purpose-built for agent-centric applications. Like GLM-4.5, it adopts the Mixture-of-Experts (MoE) architecture but with a more compact parameter size. GLM-4.5-Air also supports hybrid inference modes, offering a "thinking mode" for advanced reasoning and tool use, and a "non-thinking mode" for real-time interaction. Users can control the reasoning behaviour with the reasoning enabled boolean. Learn more in our docs
- **Разработчик:** z-ai
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 14. Mistral: Mistral Small 3.2 24B (free)
- **Размер токенов:** 1,74B tokens
- **Описание:** Mistral-Small-3.2-24B-Instruct-2506 is an updated 24B parameter model from Mistral optimized for instruction following, repetition reduction, and improved function calling. Compared to the 3.1 release, version 3.2 significantly improves accuracy on WildBench and Arena Hard, reduces infinite generations, and delivers gains in tool use and structured output tasks. It supports image and text inputs with structured outputs, function/tool calling, and strong performance across coding (HumanEval+, MBPP), STEM (MMLU, MATH, GPQA), and vision benchmarks (ChartQA, DocVQA).
- **Разработчик:** mistralai
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 15. MoonshotAI: Kimi Dev 72B (free)
- **Размер токенов:** 434M tokens
- **Описание:** Kimi-Dev-72B is an open-source large language model fine-tuned for software engineering and issue resolution tasks. Based on Qwen2.5-72B, it is optimized using large-scale reinforcement learning that applies code patches in real repositories and validates them via full test suite execution—rewarding only correct, robust completions. The model achieves 60.4% on SWE-bench Verified, setting a new benchmark among open-source models for software bug fixing and code reasoning.
- **Разработчик:** moonshotai
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 16. DeepSeek: Deepseek R1 0528 Qwen3 8B (free)
- **Размер токенов:** 1,47B tokens
- **Описание:** DeepSeek-R1-0528 is a lightly upgraded release of DeepSeek R1 that taps more compute and smarter post-training tricks, pushing its reasoning and inference to the brink of flagship models like O3 and Gemini 2.5 Pro. It now tops math, programming, and logic leaderboards, showcasing a step-change in depth-of-thought. The distilled variant, DeepSeek-R1-0528-Qwen3-8B, transfers this chain-of-thought into an 8 B-parameter form, beating standard Qwen3 8B by +10 pp and tying the 235 B "thinking" giant on AIME 2024.
- **Разработчик:** deepseek
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 17. Qwen: Qwen3 235B A22B (free)
- **Размер токенов:** 5,49B tokens
- **Описание:** Qwen3-235B-A22B is a 235B parameter mixture-of-experts (MoE) model developed by Qwen, activating 22B parameters per forward pass. It supports seamless switching between a "thinking" mode for complex reasoning, math, and code tasks, and a "non-thinking" mode for general conversational efficiency. The model demonstrates strong reasoning ability, multilingual support (100+ languages and dialects), advanced instruction-following, and agent tool-calling capabilities. It natively handles a 32K token context window and extends up to 131K tokens using YaRN-based scaling.
- **Разработчик:** qwen
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 18. Nous: DeepHermes 3 Llama 3 8B Preview (free)
- **Размер токенов:** 207M tokens
- **Описание:** DeepHermes 3 Preview is the latest version of our flagship Hermes series of LLMs by Nous Research, and one of the first models in the world to unify Reasoning (long chains of thought that improve answer accuracy) and normal LLM response modes into one model. We have also improved LLM annotation, judgement, and function calling. DeepHermes 3 Preview is one of the first LLM models to unify both "intuitive", traditional mode responses and long chain of thought reasoning responses into a single model, toggled by a system prompt.
- **Разработчик:** nousresearch
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 19. Qwen: Qwen2.5 VL 72B Instruct (free)
- **Размер токенов:** 1,26B tokens
- **Описание:** Qwen2.5-VL is proficient in recognizing common objects such as flowers, birds, fish, and insects. It is also highly capable of analyzing texts, charts, icons, graphics, and layouts within images.
- **Разработчик:** qwen
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 20. Meta: Llama 3.2 3B Instruct (free)
- **Размер токенов:** 44,7M tokens
- **Описание:** Llama 3.2 3B is a 3-billion-parameter multilingual large language model, optimized for advanced natural language processing tasks like dialogue generation, reasoning, and summarization. Designed with the latest transformer architecture, it supports eight languages, including English, Spanish, and Hindi, and is adaptable for additional languages. Trained on 9 trillion tokens, the Llama 3.2 3B model excels in instruction-following, complex reasoning, and tool use. Its balanced performance makes it ideal for applications needing accuracy and efficiency in text generation across multilingual settings. Click here for the original model card. Usage of this model is subject to Meta's Acceptable Use Policy.
- **Разработчик:** meta-llama
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 21. Mistral: Mistral Nemo (free)
- **Размер токенов:** 998M tokens
- **Описание:** A 12B parameter model with a 128k token context length built by Mistral in collaboration with NVIDIA. The model is multilingual, supporting English, French, German, Spanish, Italian, Portuguese, Chinese, Japanese, Korean, Arabic, and Hindi. It supports function calling and is released under the Apache 2.0 license.
- **Разработчик:** mistralai
- **Контекст:** 131K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 22. NVIDIA: Nemotron Nano 9B V2 (free)
- **Размер токенов:** 654M tokens
- **Описание:** NVIDIA-Nemotron-Nano-9B-v2 is a large language model (LLM) trained from scratch by NVIDIA, and designed as a unified model for both reasoning and non-reasoning tasks. It responds to user queries and tasks by first generating a reasoning trace and then concluding with a final response. The model's reasoning capabilities can be controlled via a system prompt. If the user prefers the model to provide its final answer without intermediate reasoning traces, it can be configured to do so.
- **Разработчик:** nvidia
- **Контекст:** 128K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 23. Meta: Llama 3.3 8B Instruct (free)
- **Размер токенов:** 214M tokens
- **Описание:** A lightweight and ultra-fast variant of Llama 3.3 70B, for use when quick response times are needed most.
- **Разработчик:** meta-llama
- **Контекст:** 128K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 24. Meta: Llama 4 Maverick (free)
- **Размер токенов:** 766M tokens
- **Описание:** Llama 4 Maverick 17B Instruct (128E) is a high-capacity multimodal language model from Meta, built on a mixture-of-experts (MoE) architecture with 128 experts and 17 billion active parameters per forward pass (400B total). It supports multilingual text and image input, and produces multilingual text and code output across 12 supported languages. Optimized for vision-language tasks, Maverick is instruction-tuned for assistant-like behavior, image reasoning, and general-purpose multimodal interaction. Maverick features early fusion for native multimodality and a 1 million token context window. It was trained on a curated mixture of public, licensed, and Meta-platform data, covering ~22 trillion tokens, with a knowledge cutoff in August 2024. Released on April 5, 2025 under the Llama 4 Community License, Maverick is suited for research and commercial applications requiring advanced multimodal understanding and high model throughput.
- **Разработчик:** meta-llama
- **Контекст:** 128K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 25. Meta: Llama 4 Scout (free)
- **Размер токенов:** 207M tokens
- **Описание:** Llama 4 Scout 17B Instruct (16E) is a mixture-of-experts (MoE) language model developed by Meta, activating 17 billion parameters out of a total of 109B. It supports native multimodal input (text and image) and multilingual output (text and code) across 12 supported languages. Designed for assistant-style interaction and visual reasoning, Scout uses 16 experts per forward pass and features a context length of 10 million tokens, with a training corpus of ~40 trillion tokens. Built for high efficiency and local or commercial deployment, Llama 4 Scout incorporates early fusion for seamless modality integration. It is instruction-tuned for use in multilingual chat, captioning, and image understanding tasks. Released under the Llama 4 Community License, it was last trained on data up to August 2024 and launched publicly on April 5, 2025.
- **Разработчик:** meta-llama
- **Контекст:** 128K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 26. Mistral: Mistral Small 3.1 24B (free)
- **Размер токенов:** 998M tokens
- **Описание:** Mistral Small 3.1 24B Instruct is an upgraded variant of Mistral Small 3 (2501), featuring 24 billion parameters with advanced multimodal capabilities. It provides state-of-the-art performance in text-based reasoning and vision tasks, including image analysis, programming, mathematical reasoning, and multilingual support across dozens of languages. Equipped with an extensive 128k token context window and optimized for efficient local inference, it supports use cases such as conversational agents, function calling, long-document comprehension, and privacy-sensitive deployments. The updated version is Mistral Small 3.2
- **Разработчик:** mistralai
- **Контекст:** 128K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 27. Agentica: Deepcoder 14B Preview (free)
- **Размер токенов:** 87,5M tokens
- **Описание:** DeepCoder-14B-Preview is a 14B parameter code generation model fine-tuned from DeepSeek-R1-Distill-Qwen-14B using reinforcement learning with GRPO+ and iterative context lengthening. It is optimized for long-context program synthesis and achieves strong performance across coding benchmarks, including 60.6% on LiveCodeBench v5, competitive with models like o3-Mini
- **Разработчик:** agentica-org
- **Контекст:** 96K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 28. Google: Gemma 3 27B (free)
- **Размер токенов:** 563M tokens
- **Описание:** Gemma 3 introduces multimodality, supporting vision-language input and text outputs. It handles context windows up to 128k tokens, understands over 140 languages, and offers improved math, reasoning, and chat capabilities, including structured outputs and function calling. Gemma 3 27B is Google's latest open source model, successor to Gemma 2
- **Разработчик:** google
- **Контекст:** 96K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 29. Meta: Llama 3.3 70B Instruct (free)
- **Размер токенов:** 3,4B tokens
- **Описание:** The Meta Llama 3.3 multilingual large language model (LLM) is a pretrained and instruction tuned generative model in 70B (text in/text out). The Llama 3.3 instruction tuned text only model is optimized for multilingual dialogue use cases and outperforms many of the available open source and closed chat models on common industry benchmarks. Supported languages: English, German, French, Italian, Portuguese, Hindi, Spanish, and Thai. Model Card
- **Разработчик:** meta-llama
- **Контекст:** 66K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 30. Qwen: Qwen3 4B (free)
- **Размер токенов:** 262M tokens
- **Описание:** Qwen3-4B is a 4 billion parameter dense language model from the Qwen3 series, designed to support both general-purpose and reasoning-intensive tasks. It introduces a dual-mode architecture—thinking and non-thinking—allowing dynamic switching between high-precision logical reasoning and efficient dialogue generation. This makes it well-suited for multi-turn chat, instruction following, and complex agent workflows.
- **Разработчик:** qwen
- **Контекст:** 41K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 31. Qwen: Qwen3 30B A3B (free)
- **Размер токенов:** 554M tokens
- **Описание:** Qwen3, the latest generation in the Qwen large language model series, features both dense and mixture-of-experts (MoE) architectures to excel in reasoning, multilingual support, and advanced agent tasks. Its unique ability to switch seamlessly between a thinking mode for complex reasoning and a non-thinking mode for efficient dialogue ensures versatile, high-quality performance. Significantly outperforming prior models like QwQ and Qwen2.5, Qwen3 delivers superior mathematics, coding, commonsense reasoning, creative writing, and interactive dialogue capabilities. The Qwen3-30B-A3B variant includes 30.5 billion parameters (3.3 billion activated), 48 layers, 128 experts (8 activated per task), and supports up to 131K token contexts with YaRN, setting a new standard among open-source models.
- **Разработчик:** qwen
- **Контекст:** 41K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 32. Qwen: Qwen3 8B (free)
- **Размер токенов:** 154M tokens
- **Описание:** Qwen3-8B is a dense 8.2B parameter causal language model from the Qwen3 series, designed for both reasoning-heavy tasks and efficient dialogue. It supports seamless switching between "thinking" mode for math, coding, and logical inference, and "non-thinking" mode for general conversation. The model is fine-tuned for instruction-following, agent integration, creative writing, and multilingual use across 100+ languages and dialects. It natively supports a 32K token context window and can extend to 131K tokens with YaRN scaling.
- **Разработчик:** qwen
- **Контекст:** 41K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 33. Qwen: Qwen3 14B (free)
- **Размер токенов:** 653M tokens
- **Описание:** Qwen3-14B is a dense 14.8B parameter causal language model from the Qwen3 series, designed for both complex reasoning and efficient dialogue. It supports seamless switching between a "thinking" mode for tasks like math, programming, and logical inference, and a "non-thinking" mode for general-purpose conversation. The model is fine-tuned for instruction-following, agent tool use, creative writing, and multilingual tasks across 100+ languages and dialects. It natively handles 32K token contexts and can extend to 131K tokens using YaRN-based scaling.
- **Разработчик:** qwen
- **Контекст:** 41K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 34. MoonshotAI: Kimi K2 0711 (free)
- **Размер токенов:** 106M tokens
- **Описание:** Kimi K2 Instruct is a large-scale Mixture-of-Experts (MoE) language model developed by Moonshot AI, featuring 1 trillion total parameters with 32 billion active per forward pass. It is optimized for agentic capabilities, including advanced tool use, reasoning, and code synthesis. Kimi K2 excels across a broad range of benchmarks, particularly in coding (LiveCodeBench, SWE-bench), reasoning (ZebraLogic, GPQA), and tool-use (Tau2, AceBench) tasks. It supports long-context inference up to 128K tokens and is designed with a novel training stack that includes the MuonClip optimizer for stable large-scale MoE training.
- **Разработчик:** moonshotai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 35. Venice: Uncensored (free)
- **Размер токенов:** 1,96B tokens
- **Описание:** Venice Uncensored Dolphin Mistral 24B Venice Edition is a fine-tuned variant of Mistral-Small-24B-Instruct-2501, developed by dphn.ai in collaboration with Venice.ai. This model is designed as an "uncensored" instruct-tuned LLM, preserving user control over alignment, system prompts, and behavior. Intended for advanced and unrestricted use cases, Venice Uncensored emphasizes steerability and transparent behavior, removing default safety and alignment layers typically found in mainstream assistant models.
- **Разработчик:** cognitivecomputations
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 36. Tencent: Hunyuan A13B Instruct (free)
- **Размер токенов:** 27,1M tokens
- **Описание:** Hunyuan-A13B is a 13B active parameter Mixture-of-Experts (MoE) language model developed by Tencent, with a total parameter count of 80B and support for reasoning via Chain-of-Thought. It offers competitive benchmark performance across mathematics, science, coding, and multi-turn reasoning tasks, while maintaining high inference efficiency via Grouped Query Attention (GQA) and quantization support (FP8, GPTQ, etc.).
- **Разработчик:** tencent
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 37. Mistral: Devstral Small 2505 (free)
- **Размер токенов:** 195M tokens
- **Описание:** Devstral-Small-2505 is a 24B parameter agentic LLM fine-tuned from Mistral-Small-3.1, jointly developed by Mistral AI and All Hands AI for advanced software engineering tasks. It is optimized for codebase exploration, multi-file editing, and integration into coding agents, achieving state-of-the-art results on SWE-Bench Verified (46.8%). Devstral supports a 128k context window and uses a custom Tekken tokenizer. It is text-only, with the vision encoder removed, and is suitable for local deployment on high-end consumer hardware (e.g., RTX 4090, 32GB RAM Macs). Devstral is best used in agentic workflows via the OpenHands scaffold and is compatible with inference frameworks like vLLM, Transformers, and Ollama. It is released under the Apache 2.0 license.
- **Разработчик:** mistralai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 38. Shisa AI: Shisa V2 Llama 3.3 70B (free)
- **Размер токенов:** 206M tokens
- **Описание:** Shisa V2 Llama 3.3 70B is a bilingual Japanese-English chat model fine-tuned by Shisa.AI on Meta's Llama-3.3-70B-Instruct base. It prioritizes Japanese language performance while retaining strong English capabilities. The model was optimized entirely through post-training, using a refined mix of supervised fine-tuning (SFT) and DPO datasets including regenerated ShareGPT-style data, translation tasks, roleplaying conversations, and instruction-following prompts. Unlike earlier Shisa releases, this version avoids tokenizer modifications or extended pretraining. Shisa V2 70B achieves leading Japanese task performance across a wide range of custom and public benchmarks, including JA MT Bench, ELYZA 100, and Rakuda. It supports a 128K token context length and integrates smoothly with inference frameworks like vLLM and SGLang. While it inherits safety characteristics from its base model, no additional alignment was applied. The model is intended for high-performance bilingual chat, instruction following, and translation tasks across JA/EN.
- **Разработчик:** shisa-ai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 39. ArliAI: QwQ 32B RpR v1 (free)
- **Размер токенов:** 42,8M tokens
- **Описание:** QwQ-32B-ArliAI-RpR-v1 is a 32B parameter model fine-tuned from Qwen/QwQ-32B using a curated creative writing and roleplay dataset originally developed for the RPMax series. It is designed to maintain coherence and reasoning across long multi-turn conversations by introducing explicit reasoning steps per dialogue turn, generated and refined using the base model itself. The model was trained using RS-QLORA+ on 8K sequence lengths and supports up to 128K context windows (with practical performance around 32K). It is optimized for creative roleplay and dialogue generation, with an emphasis on minimizing cross-context repetition while preserving stylistic diversity.
- **Разработчик:** arliai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 40. Google: Gemma 3 4B (free)
- **Размер токенов:** 10,1M tokens
- **Описание:** Gemma 3 introduces multimodality, supporting vision-language input and text outputs. It handles context windows up to 128k tokens, understands over 140 languages, and offers improved math, reasoning, and chat capabilities, including structured outputs and function calling.
- **Разработчик:** google
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 41. Google: Gemma 3 12B (free)
- **Размер токенов:** 33,3M tokens
- **Описание:** Gemma 3 introduces multimodality, supporting vision-language input and text outputs. It handles context windows up to 128k tokens, understands over 140 languages, and offers improved math, reasoning, and chat capabilities, including structured outputs and function calling. Gemma 3 12B is the second largest in the family of Gemma 3 models after Gemma 3 27B
- **Разработчик:** google
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 42. Dolphin3.0 Mistral 24B (free)
- **Размер токенов:** 186M tokens
- **Описание:** Dolphin 3.0 is the next generation of the Dolphin series of instruct-tuned models. Designed to be the ultimate general purpose local model, enabling coding, math, agentic, function calling, and general use cases. Dolphin aims to be a general purpose instruct model, similar to the models behind ChatGPT, Claude, Gemini. Part of the Dolphin 3.0 Collection Curated and trained by Eric Hartford, Ben Gitter, BlouseJury and Cognitive Computations
- **Разработчик:** cognitivecomputations
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 43. Mistral: Mistral Small 3 (free)
- **Размер токенов:** 85,2M tokens
- **Описание:** Mistral Small 3 is a 24B-parameter language model optimized for low-latency performance across common AI tasks. Released under the Apache 2.0 license, it features both pre-trained and instruction-tuned versions designed for efficient local deployment. The model achieves 81% accuracy on the MMLU benchmark and performs competitively with larger models like Llama 3.3 70B and Qwen 32B, while operating at three times the speed on equivalent hardware. Read the blog post about the model here.
- **Разработчик:** mistralai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 44. Qwen2.5 Coder 32B Instruct (free)
- **Размер токенов:** 378M tokens
- **Описание:** Qwen2.5-Coder is the latest series of Code-Specific Qwen large language models (formerly known as CodeQwen). Qwen2.5-Coder brings the following improvements upon CodeQwen1.5: - Significantly improvements in code generation, code reasoning and code fixing. - A more comprehensive foundation for real-world applications such as Code Agents. Not only enhancing coding capabilities but also maintaining its strengths in mathematics and general competencies. To read more about its evaluation results, check out Qwen 2.5 Coder's blog.
- **Разработчик:** qwen
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 45. Qwen2.5 72B Instruct (free)
- **Размер токенов:** 294M tokens
- **Описание:** Qwen2.5 72B is the latest series of Qwen large language models. Qwen2.5 brings the following improvements upon Qwen2: - Significantly more knowledge and has greatly improved capabilities in coding and mathematics, thanks to our specialized expert models in these domains. - Significant improvements in instruction following, generating long texts (over 8K tokens), understanding structured data (e.g, tables), and generating structured outputs especially JSON. More resilient to the diversity of system prompts, enhancing role-play implementation and condition-setting for chatbots. - Long-context Support up to 128K tokens and can generate up to 8K tokens. - Multilingual support for over 29 languages, including Chinese, English, French, Spanish, Portuguese, German, Italian, Russian, Japanese, Korean, Vietnamese, Thai, Arabic, and more. Usage of this model is subject to Tongyi Qianwen LICENSE AGREEMENT.
- **Разработчик:** qwen
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 46. Mistral: Mistral 7B Instruct (free)
- **Размер токенов:** 327M tokens
- **Описание:** A high-performing, industry-standard 7.3B parameter model, with optimizations for speed and context length. Mistral 7B Instruct has multiple version variants, and this is intended to be the latest version.
- **Разработчик:** mistralai
- **Контекст:** 33K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 47. Qwen: Qwen2.5 VL 32B Instruct (free)
- **Размер токенов:** 181M tokens
- **Описание:** Qwen2.5-VL-32B is a multimodal vision-language model fine-tuned through reinforcement learning for enhanced mathematical reasoning, structured outputs, and visual problem-solving capabilities. It excels at visual analysis tasks, including object recognition, textual interpretation within images, and precise event localization in extended videos. Qwen2.5-VL-32B demonstrates state-of-the-art performance across multimodal benchmarks such as MMMU, MathVista, and VideoMME, while maintaining strong reasoning and clarity in text-based tasks like MMLU, mathematical problem-solving, and code generation.
- **Разработчик:** qwen
- **Контекст:** 16K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 48. Google: Gemma 3n 2B (free)
- **Размер токенов:** 30M tokens
- **Описание:** Gemma 3n E2B IT is a multimodal, instruction-tuned model developed by Google DeepMind, designed to operate efficiently at an effective parameter size of 2B while leveraging a 6B architecture. Based on the MatFormer architecture, it supports nested submodels and modular composition via the Mix-and-Match framework. Gemma 3n models are optimized for low-resource deployment, offering 32K context length and strong multilingual and reasoning performance across common benchmarks. This variant is trained on a diverse corpus including code, math, web, and multimodal data.
- **Разработчик:** google
- **Контекст:** 8K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 49. Google: Gemma 3n 4B (free)
- **Размер токенов:** 13,7M tokens
- **Описание:** Gemma 3n E4B-it is optimized for efficient execution on mobile and low-resource devices, such as phones, laptops, and tablets. It supports multimodal inputs—including text, visual data, and audio—enabling diverse tasks such as text generation, speech recognition, translation, and image analysis. Leveraging innovations like Per-Layer Embedding (PLE) caching and the MatFormer architecture, Gemma 3n dynamically manages memory usage and computational load by selectively activating model parameters, significantly reducing runtime resource requirements. This model supports a wide linguistic range (trained in over 140 languages) and features a flexible 32K token context window. Gemma 3n can selectively load parameters, optimizing memory and computational efficiency based on the task or device capabilities, making it well-suited for privacy-focused, offline-capable applications and on-device AI solutions. Read more in the blog post
- **Разработчик:** google
- **Контекст:** 8K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 50. DeepSeek: R1 Distill Llama 70B (free)
- **Размер токенов:** 1,65B tokens
- **Описание:** DeepSeek R1 Distill Llama 70B is a distilled large language model based on Llama-3.3-70B-Instruct, using outputs from DeepSeek R1. The model combines advanced distillation techniques to achieve high performance across multiple benchmarks, including: - AIME 2024 pass@1: 70.0 - MATH-500 pass@1: 94.5 - CodeForces Rating: 1633 The model leverages fine-tuning from DeepSeek R1's outputs, enabling competitive performance comparable to larger frontier models.
- **Разработчик:** deepseek
- **Контекст:** 8K context
- **Цена:** $0/M input tokens, $0/M output tokens

## 51. Google: Gemma 2 9B (free)
- **Размер токенов:** 38,4M tokens
- **Описание:** Gemma 2 9B by Google is an advanced, open-source language model that sets a new standard for efficiency and performance in its size class. Designed for a wide variety of tasks, it empowers developers and researchers to build innovative applications, while maintaining accessibility, safety, and cost-effectiveness. See the launch announcement for more details. Usage of Gemma is subject to Google's Gemma Terms of Use.
- **Разработчик:** google
- **Контекст:** 8K context
- **Цена:** $0/M input tokens, $0/M output tokens