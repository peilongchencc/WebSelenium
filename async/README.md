# selenium 异步:

由于selenium是同步操作，难以转异步，做并行化需要 `asyncio` 和 `ThreadPoolExecutor` 结合使用，代价较大，故笔者就没有尝试，这里只记录相关的概念点，读者有兴趣可以自己去尝试。<br>
- [selenium 异步:](#selenium-异步)
  - [ThreadPoolExecutor 和 ProcessPoolExecutor 是什么？](#threadpoolexecutor-和-processpoolexecutor-是什么)
    - [ThreadPoolExecutor](#threadpoolexecutor)
    - [ProcessPoolExecutor](#processpoolexecutor)
    - [使用示例](#使用示例)
      - [使用 ThreadPoolExecutor](#使用-threadpoolexecutor)
      - [使用 ProcessPoolExecutor](#使用-processpoolexecutor)
  - [不可以单独使用 `asyncio` 构建 selenium 的异步吗？](#不可以单独使用-asyncio-构建-selenium-的异步吗)


## ThreadPoolExecutor 和 ProcessPoolExecutor 是什么？

`ThreadPoolExecutor` 和 `ProcessPoolExecutor` 都是 Python `concurrent.futures` 模块中的类，用于简化多线程和多进程编程。这两个执行器（Executor）提供了一个高层次的接口来异步执行可调用对象，并通过工作线程或工作进程池来管理它们的执行。<br>


### ThreadPoolExecutor

`ThreadPoolExecutor` 是一个线程池，用于执行并发的线程任务。它通过创建一个线程池来管理线程，这样你就可以将任务提交到线程池中，而不必每次都手动创建和管理线程。<br>

使用线程池可以有效地重用已存在的线程，减少线程创建和销毁的开销。线程池尤其适用于执行大量的、轻量级的操作，如网络请求或其他I/O密集型任务。<br>

### ProcessPoolExecutor

`ProcessPoolExecutor` 与 `ThreadPoolExecutor` 类似，不过它是使用进程池而不是线程池。在 Python 中，由于全局解释器锁（GIL）的存在，多线程并不总是能有效利用多核处理器。<br>

`ProcessPoolExecutor` 通过创建多个进程来克服这个问题，每个进程都有自己的 Python 解释器和内存空间，因此可以实现真正的并行计算。这对于计算密集型任务特别有用，例如大规模数值计算、图像处理等。<br>

### 使用示例

下面是使用 `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 的基本示例：<br>

#### 使用 ThreadPoolExecutor

```python
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/', 'http://www.cnn.com/', 'http://europe.wsj.com/', 'http://www.bbc.co.uk/']

def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = {executor.submit(load_url, url, 10): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
            print('%r page is %d bytes' % (url, len(data)))
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
```

#### 使用 ProcessPoolExecutor

```python
import concurrent.futures
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

numbers = [1297337, 1116281, 104395303, 472882027, 533000389]

with concurrent.futures.ProcessPoolExecutor() as executor:
    for number, prime in zip(numbers, executor.map(is_prime, numbers)):
        print('%d is prime: %s' % (number, prime))
```

这些示例演示了如何在并发编程中使用线程和进程池来提高效率和性能。<br>


## 不可以单独使用 `asyncio` 构建 selenium 的异步吗？

在处理 Selenium 的场景中，直接使用 `asyncio` 来进行异步操作有一些限制，因为 Selenium 是一个固有的同步库，它的操作（如加载网页、查找元素等）会阻塞调用线程，直到操作完成。<br>

> asyncio 是一个单线程多协程的实现库。

`asyncio` 是专门设计来处理异步和非阻塞 I/O 的，例如网络请求和文件读写，但它并不能直接将同步代码变为异步代码。<br>

🚨🚨🚨然而，有一种方法可以在使用 `asyncio` 的同时处理 Selenium 的同步行为，那就是通过 `concurrent.futures` 中的线程池或进程池来运行这些同步操作。<br>

这样做的主要目的是将阻塞操作放在单独的线程或进程中执行，从而避免阻塞 `asyncio` 的事件循环。这种方法虽然不是纯粹的 `asyncio` 使用方式，但它是在当前技术栈下实现异步 Web 浏览操作的可行解决方案。<br>

‼️‼️‼️直接使用 `asyncio`，没有其他辅助的库，是无法改造 Selenium 的操作为异步的，因为这需要 Selenium 库本身支持异步操作，或者需要对其底层实现进行重写，这通常是不切实际的。<br>

总之，为了在你的项目中利用 `asyncio` 提高性能，你需要结合使用 `concurrent.futures.ThreadPoolExecutor` 或者其它能够在后台执行阻塞操作的方法，这是在不改变 Selenium 库的前提下最有效的方案。<br>

如果你的应用非常依赖于性能和并发，可能需要考虑使用其他原生支持异步的 Web 抓取工具(如 playwright)。<br>

❤️笔者就转战了 playwright，这里不是说 selenium 没用，而是各有各的使用场景。比如你项目组的代码都是同步的，你怎么把 playwright 嵌入项目，这时候明显使用 selenium 更好。至于耗时问题，可以采用后台运行，将爬取结果入库，留待其他人取用即可。<br>