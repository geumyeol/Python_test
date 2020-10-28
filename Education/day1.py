
def is_palindrome(word):
    # 코드를 입력하세요.
    length = len(word)-1

    for c in range(0, int(length/2)+1):
        # print (word[c], word[length-c])
        if word[c] != word[length-c]:
            return False

    return True

# 테스트
print(is_palindrome("racecar"))
print(is_palindrome("stars"))
print(is_palindrome("토마토"))
print(is_palindrome("kayak"))
print(is_palindrome("hello"))