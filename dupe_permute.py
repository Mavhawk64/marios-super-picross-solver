class GFG:
    def __init__(self):
        self.nums = []
        self.curr = []
        self.ans = []
        self.visited = []

    def backtrack(self):
        # If current permutation is complete
        if len(self.curr) == len(self.nums):
            self.ans.append(tuple(self.curr.copy()))

        # Traverse the input list
        for i in range(len(self.nums)):
            # If index is already visited
            if self.visited[i]:
                continue
            
            # If the number is duplicate
            if i > 0 and self.nums[i] == self.nums[i - 1] and not self.visited[i - 1]:
                continue
            
            # Set visited[i] flag as True
            self.visited[i] = True

            # Append nums[i] to current list
            self.curr.append(self.nums[i])

            # Recursive function call
            self.backtrack()

            # Backtrack to the previous state by unsetting visited[i]
            self.visited[i] = False

            # Remove nums[i] from the end of the list
            self.curr.pop()

    def permuteDuplicates(self):
        # Sort the list
        self.nums.sort()

        for _ in self.nums:
            self.visited.append(False)

        # Find the distinct permutations of nums
        self.backtrack()

        return self.ans

    def getDistinctPermutations(self):
        self.ans = self.permuteDuplicates()
        return self.ans
