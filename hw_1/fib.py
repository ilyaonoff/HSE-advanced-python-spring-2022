def fibonacci(n):
    ans = [0, 1]
    for _ in range(n - 1):
        ans.append(ans[-2] + ans[-1])
    return ans[1:]
