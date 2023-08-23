from classes import CQueue

def list_equal(l1, l2):
    if len(l1) == len(l2):
        for i in range(len(l1)):
            if l1[i] == l2[i]:
                pass
            else:
                print(l1[i], "!=", l2[i])
                return False
    else:
        return False
    return True

def run_tests():
    # Test 1: Insertion
    t1 = CQueue(4)
    t1.put(1)
    expected = [1,0,0,0]
    if list_equal(expected, t1.listy):
        print("T1 passed")
    else:
        print("T1 failed")

    # Test 2: Rollover
    t2 = CQueue(4)
    t2.put(1)
    t2.put(2)
    t2.put(3)
    t2.put(4)
    t2.put(5)
    expected = [5,2,3,4]
    if list_equal(expected, t2.listy):
        print("T2 passed")
    else:
        print("T2 failed")       

    # Test 3: Average
    t3 = CQueue(4)
    t3.put(1)
    t3.put(2)
    t3.put(3)
    t3.put(4)
    expected_avg = 2.5
    if 0.01 < abs(expected_avg - t3.get_avg()):
        print("T3 passed")
    else:
        print("T3 failed")

    # Test 4: Average Rollover
    t4 = CQueue(4)
    t4.put(1)
    t4.put(2)
    t4.put(3)
    t4.put(4)
    t4.put(5)
    expected_avg = 3.5
    if 0.01 < abs(expected_avg - t4.get_avg()):
        print("T4 passed")
    else:
        print("T4 failed")


if __name__ == "__main__":
    run_tests()