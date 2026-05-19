class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def getIntersectionNode(headA, headB):
    # Boundary check
    if not headA or not headB:
        return None
        
    pA = headA
    pB = headB
    
    # Loop continues until the two pointers meet
    while pA != pB:
        # If pointer A reaches the end, switch to head B. Otherwise, move to next.
        pA = pB if pA is None else pA.next
        
        # If pointer B reaches the end, switch to head A. Otherwise, move to next.
        pB = headA if pB is None else pB.next
        
    # Either they met at the intersection node, or both are None (no intersection)
    return pA