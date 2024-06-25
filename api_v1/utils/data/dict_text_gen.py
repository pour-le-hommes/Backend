def get_text_gen_dict():
    model_dict = {
        0: "@cf/qwen/qwen1.5-0.5b-chat",
        1: "@cf/google/gemma-2b-it-lora",
        2: "@hf/nexusflow/starling-lm-7b-beta",
        3: "@cf/meta/llama-3-8b-instruct",
        4: "@hf/thebloke/llamaguard-7b-awq",
        5: "@hf/thebloke/neural-chat-7b-v3-1-awq",
        6: "@cf/meta/llama-2-7b-chat-fp16",
        7: "@cf/mistral/mistral-7b-instruct-v0.1",
        8: "@cf/mistral/mistral-7b-instruct-v0.2-lora",
        9: "@cf/tinyllama/tinyllama-1.1b-chat-v1.0",
        10: "@hf/mistral/mistral-7b-instruct-v0.2",
        11: "@cf/fblgit/una-cybertron-7b-v2-bf16",
        12: "@cf/thebloke/discolm-german-7b-v1-awq",
        13: "@cf/meta/llama-2-7b-chat-int8",
        14: "@hf/thebloke/mistral-7b-instruct-v0.1-awq",
        15: "@cf/qwen/qwen1.5-7b-chat-awq",
        16: "@hf/thebloke/llama-2-13b-chat-awq",
        17: "@hf/thebloke/deepseek-coder-6.7b-base-awq",
        18: "@cf/meta-llama/llama-2-7b-chat-hf-lora",
        19: "@hf/thebloke/openhermes-2.5-mistral-7b-awq",
        20: "@cf/mistral/mistral-7b-instruct-v0.1-vllm",
        21: "@hf/thebloke/deepseek-coder-6.7b-instruct-awq",
        22: "@cf/deepseek-ai/deepseek-math-7b-instruct",
        23: "@cf/tiiuae/falcon-7b-instruct",
        24: "@hf/nousresearch/hermes-2-pro-mistral-7b",
        25: "@hf/thebloke/zephyr-7b-beta-awq",
        26: "@cf/google/gemma-7b-it-lora",
        27: "@cf/qwen/qwen1.5-1.8b-chat",
        28: "@cf/meta/llama-3-8b-instruct-awq",
        29: "@cf/defog/sqlcoder-7b-2",
        30: "@cf/microsoft/phi-2",
        31: "@hf/meta-llama/meta-llama-3-8b-instruct",
        32: "@hf/google/gemma-7b-it",
        33: "@cf/qwen/qwen1.5-14b-chat-awq",
        34: "@cf/openchat/openchat-3.5-0106"
    }
    return model_dict

def get_speech_dict():
    model_dict = {
        0: "@cf/openai/whisper",
        1: "@cf/openai/whisper-sherpa",
        2: "@cf/openai/whisper-tiny-en"
    }
    return model_dict