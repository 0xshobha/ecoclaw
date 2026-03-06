import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def test_models():
    client = AsyncOpenAI(
        api_key=os.getenv("ZAI_API_KEY"),
        base_url=os.getenv("ZAI_API_BASE", "https://open.bigmodel.cn/api/paas/v4")
    )
    
    for model in ["glm-4.5", "glm-5", "glm-4.5-air"]:
        try:
            print(f"Testing {model}...")
            resp = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hello"}],
                max_tokens=10
            )
            print(f"SUCCESS with {model}! Response: {resp.choices[0].message.content}")
            return model
        except Exception as e:
            print(f"Failed {model}: {e}")

if __name__ == "__main__":
    asyncio.run(test_models())
