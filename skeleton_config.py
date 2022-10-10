from androguard.misc import AnalyzeAPK, APK

#TARGET = "/home/weather/Desktop/AG/aptandroid/target/UnCrackable-Level1.apk"
# TARGET = "/home/weather/Desktop/AG/aptandroid/target/HonSystemService.apk"
TARGET = "/home/weather/Desktop/AG/aptandroid/target/HDWallpaper.apk"
# TARGET = "/home/weather/Desktop/AG/aptandroid/target/Mediacode.apk"

#기능 출력 요소들
#권한 출력, 엑티비티 내역 출력, 패키지 정보, 클래스 정보, 메소드 바이트 코드 출력, 문자열, opcode 활용된 instrucment 개수,

#해야하는 것
# 클래스 중 api 확인,, obfuscation(packing??), database 존재 유무, 컴파일 정보

## 권한 출력 및 관련 권한 메소드 출력
def permission(a,d,dx,FLAG=1):
    print(f"[*]PERMISSION EXTRACTING")
    api_level = a.get_effective_target_sdk_version()
    
    General_Permission = a.get_permissions()
    if FLAG:
        print(f"permission : {General_Permission}")
    
    for i,j in dx.get_permissions():
        flag=0
        for k in j:
            if k in General_Permission:
                flag=1
                break
        if flag:
            print(f"[*]{j}\n\t[+]{i}")

    return General_Permission


## 활동 내역 출력
def activity(a,d,dx,flag=1):
    if flag:
        print(f"[*]Activity Extracting")
    start_activity = a.get_main_activities()
    if flag:
        print(f"Starting with {start_activity}")
    activity = a.get_activities()
    if flag:
        print(f"Kind of Activity: {activity}\n")
    return activity

## 서비스 관련 출력
def services(a,d,dx,flag=1):
    if flag:
        print(f"[*]Services Extracting")
    service = a.get_services()
    if flag:
        print(f"service list:{service}\n")
    return service
    
## receivers 관련 출력
def receivers(a,d,dx,flag=1):
    if flag:
        print(f"[*]receivers Extracting")
    receiver = a.get_receivers()
    if flag:
        print(f"receiver list: {receiver}\n")
    return receiver


##패키지 정보
def package(a,d,dx):
    print(f"[*]Package Extracting")
    package = a.get_package()
    print(f"{package}\n")
    return package

##클래스 정보 출력
def classes(a,d,dx):
    print(f"[*]Class Extracting")
    classes = dx.get_classes()
    classes = list(classes)
    for i in classes:
        for meth in i.get_methods():
            print(f"inside method {meth.name}")
            for _, call, _ in meth.get_xref_to():
                print(f"  calling -> {call.class_name} -- {call.name}")
    print("")
    return classes

##method 바이트 코드
def method_raw(a,d,dx):
    print(f"[*]method Extracting")
    classes = dx.get_classes()
    classes = list(classes)
    for i in classes:
        for meth in i.get_methods():
            if meth.is_external():
                continue
            m = meth.get_method()
            if m.get_code():
                print(m.get_code().get_bc().get_raw())
    print("")

## 문자열 정보 확인
def string(a,d,dx):
    print(f"[*]Class Extracting")
    string = dx.strings
    string = list(string)
    for i in string:
        for _,meth in dx.strings[i].get_xref_from():
            print(f"Used in: {meth.class_name} -- {meth.name} -- {i}")
    return string        

##opcode 개수
def opcode_cnt(a,d,dx):
    print(f"[*]Opcode Extracting")
    from collections import defaultdict
    from operator import itemgetter
    c = defaultdict(int)

    for method in dx.get_methods():
        if method.is_external():
            continue
        m = method.get_method()
        for ins in m.get_instructions():
            c[(ins.get_op_value(), ins.get_name())] += 1

    for k, v in sorted(c.items(), key=itemgetter(1), reverse=True)[:]:
        print(k, '-->',  v)

##opcode 순서
def opcode_seq(a,d,dx):
    for method in dx.get_methods():
        if method.is_external():
            continue
        m = method.get_method()
        
        print(method)
        for idx, ins in m.get_instructions_idx():
            print(idx, ins.get_op_value(), ins.get_name(), ins.get_output())


##intent요소 사용하는 테그 활용
def intent(a,d,dx):
    print("ACTIVITY_INTENT EXTRACTING")
    for i in activity(a,d,dx,0):
        print(f"[+]activity{i}")
        for i,j in a.get_intent_filters("activity",i).items():
            print(f"\t{i} : {j}")
    print("")
        
    print("SERVICE_INTENT EXTRACTING")
    for i in services(a,d,dx,0):
        print(f"[+]services{i}")
        for i,j in a.get_intent_filters("service",i).items():
            print(f"\t{i} : {j}")
    print("")
    
    print("RECEIVER_INTENT EXTRACTING")
    for i in receivers(a,d,dx,0):
        print(f"[+]receiviers{i}")
        for i,j in a.get_intent_filters("receivier",i).items():
            print(f"\t{i} : {j}")
    print("")

## res 파일 내부에 들어있는 파일들
def file_res(a,d,dx):
    for i in a.get_files():
        if "res/" in i:
            print(i)
    print("")
    
        

if __name__=="__main__":
    ## 전반적 분석 진행
    a,d,dx = AnalyzeAPK(TARGET)
    
    # PERMISSION = permission(a,d,dx)
    
    # ACTIVITY = activity(a,d,dx)
    
    # SERVICE =  services(a,d,dx)
    
    # RECEIVER = receivers(a,d,dx)
    
    # PACKAGE = package(a,d,dx)
    
    # classes = classes(a,d,dx)
    
    # method_raw = method_raw(a,d,dx)
    
    # string = string(a,d,dx)
    
    # opcode = opcode_cnt(a,d,dx)
    
    opcode_seq(a,d,dx)
    
    # intent(a,d,dx)
   
    # file_res(a,d,dx)
    
    


