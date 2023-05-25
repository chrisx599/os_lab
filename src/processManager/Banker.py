"""
Writen by Liang Zhengyang
"""

class BankerAlgorithm:
    def __init__(self, available, max_claim, allocation, need):
        self.available = available
        self.max_claim = max_claim
        self.allocation = allocation
        self.need = need
        self.num_processes = len(available)
        self.num_resources = len(available)

    def is_safe_state(self):
        work = self.available.copy()
        finish = [False] * self.num_processes
        sequence = []

        while True:
            # 搜索一个满足条件的进程
            found = False
            for process in range(self.num_processes):
                if not finish[process] and self.check_resources_available(process, work):
                    # 分配资源给进程
                    for resource in range(self.num_resources):
                        work[resource] += self.allocation[process][resource]
                    finish[process] = True
                    sequence.append(process)
                    found = True
                    break

            if not found:
                # 没有找到满足条件的进程
                break

        return all(finish), sequence

    def check_resources_available(self, process, work):
        for resource in range(self.num_resources):
            if self.need[process][resource] > work[resource]:
                return False
        return True


# 测试案例
if __name__ == '__main__':
    available = [3, 3, 2]  # 可用资源数目
    max_claim = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]  # 进程对各资源的最大需求
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]  # 进程已分配的资源
    need = [
        [7, 4, 3],
        [1, 2, 2],
        [6, 0, 0],
        [0, 1, 1],
        [4, 3, 1]
    ]  # 进程还需要的资源

    banker = BankerAlgorithm(available, max_claim, allocation, need)
    safe, sequence = banker.is_safe_state()

    if safe:
        print("系统处于安全状态，安全序列为:", sequence)
    else:
        print("系统处于不安全状态")
