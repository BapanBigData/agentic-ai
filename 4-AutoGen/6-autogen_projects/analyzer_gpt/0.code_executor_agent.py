import asyncio
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='tmp',
        timeout=120
    )

    code_executor_agent = CodeExecutorAgent(
        name = 'CodeExecutorAgent',
        code_executor=docker,
    )

    task = TextMessage(
        content='''Here is the code 
```python
print("hello world, how are you?")
```

```python
def add_two_integers(a: int, b: int) -> int:
    """
    Returns the sum of two integers.

    Parameters:
    a (int): First integer
    b (int): Second integer

    Returns:
    int: Sum of a and b
    """
    return a + b
    
result = add_two_integers(5, 7)
print("The sum of two integers is:", result)
```

```python
def factorial(n: int) -> int:
    """
    Recursively calculates the factorial of a non-negative integer n.

    Parameters:
    n (int): The number to compute the factorial of. Must be >= 0.

    Returns:
    int: Factorial of n

    Raises:
    ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

n = 5
res = factorial(5)
print(f"factorial of {n} is:", res)
```
    ''',
    source='user'
    )

    await docker.start()

    result = await code_executor_agent.on_messages(
        messages=[task],
        cancellation_token=CancellationToken()
    )

    print("The result is", result)
    print('\n')
    print(result.chat_message.content)

    await docker.stop()
    

if (__name__=='__main__'):
    asyncio.run(main())