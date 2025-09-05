def merge_sorted_arrays(arr1, arr2):
    """
    دمج مصفوفتين مرتبتين في مصفوفة واحدة مرتبة
    
    التعقيد الزمني: O(n + m) حيث n و m هما أطوال المصفوفتين
    التعقيد المكاني: O(n + m) للمصفوفة الناتجة
    
    Args:
        arr1: المصفوفة الأولى المرتبة
        arr2: المصفوفة الثانية المرتبة
    
    Returns:
        مصفوفة مدموجة ومرتبة
    """
    # مؤشرين للتنقل في المصفوفتين
    i, j = 0, 0
    merged = []
    
    # دمج العناصر بالترتيب الصحيح
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            merged.append(arr1[i])
            i += 1
        else:
            merged.append(arr2[j])
            j += 1
    
    # إضافة العناصر المتبقية من المصفوفة الأولى
    while i < len(arr1):
        merged.append(arr1[i])
        i += 1
    
    # إضافة العناصر المتبقية من المصفوفة الثانية
    while j < len(arr2):
        merged.append(arr2[j])
        j += 1
    
    return merged


def merge_in_place(arr1, m, arr2, n):
    """
    دمج مصفوفتين في المكان (in-place) - مفيد عندما تكون المصفوفة الأولى كبيرة بما يكفي
    
    Args:
        arr1: المصفوفة الأولى (يجب أن تكون كبيرة بما يكفي لاستيعاب العناصر)
        m: عدد العناصر الفعلية في arr1
        arr2: المصفوفة الثانية
        n: عدد العناصر في arr2
    """
    # البدء من النهاية لتجنب الكتابة فوق البيانات
    i = m - 1  # آخر عنصر في arr1
    j = n - 1  # آخر عنصر في arr2
    k = m + n - 1  # آخر موضع في arr1 المدمجة
    
    while i >= 0 and j >= 0:
        if arr1[i] > arr2[j]:
            arr1[k] = arr1[i]
            i -= 1
        else:
            arr1[k] = arr2[j]
            j -= 1
        k -= 1
    
    # إضافة العناصر المتبقية من arr2
    while j >= 0:
        arr1[k] = arr2[j]
        j -= 1
        k -= 1


# أمثلة على الاستخدام
if __name__ == "__main__":
    print("=== خوارزمية دمج المصفوفات المرتبة ===")
    print()
    
    # مثال 1: الدمج العادي
    array1 = [1, 3, 5, 7, 9]
    array2 = [2, 4, 6, 8, 10, 12]
    
    print("المصفوفة الاولى:", array1)
    print("المصفوفة الثانية:", array2)
    
    result = merge_sorted_arrays(array1, array2)
    print("النتيجة المدمجة:", result)
    print()
    
    # مثال 2: مصفوفات بأطوال مختلفة
    array3 = [1, 5, 9, 10, 15, 20]
    array4 = [2, 3, 8, 13]
    
    print("المصفوفة الثالثة:", array3)
    print("المصفوفة الرابعة:", array4)
    
    result2 = merge_sorted_arrays(array3, array4)
    print("النتيجة المدمجة:", result2)
    print()
    
    # مثال 3: الدمج في المكان
    array5 = [1, 2, 3, 0, 0, 0]  # المساحة الاضافية للدمج
    array6 = [2, 5, 6]
    m, n = 3, 3
    
    print("قبل الدمج في المكان:", array5)
    print("المصفوفة للدمج:", array6)
    
    merge_in_place(array5, m, array6, n)
    print("بعد الدمج في المكان:", array5)
    print()
    
    # مثال 4: حالات خاصة
    empty_array = []
    single_array = [42]
    
    print("=== حالات خاصة ===")
    print("دمج مصفوفة فارغة مع [42]:", merge_sorted_arrays(empty_array, single_array))
    print("دمج [1,2,3] مع مصفوفة فارغة:", merge_sorted_arrays([1,2,3], empty_array))