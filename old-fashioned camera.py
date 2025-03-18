import cv2
import numpy as np

# 카메라 기본 캠 불러오기
cap = cv2.VideoCapture(0)

# 동영상 파일 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정 avi로 저장
out = None  # 비디오 저장 객체, 초기 상태 None

recording = False  # 녹화 상태 
gray_mode = False  # 흑백 모드 
low_quality_mode = False  # 저화질 모드 
blink_counter = 0  # 녹화 중일 때 빨간 점 깜빡이게, 제어 변수

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    output_frame = frame.copy()  # 녹화용 원본 프레임 저장

    # 흑백 모드 적용
    if gray_mode:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # 컬러 채널 유지
        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_BGR2GRAY)
        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_GRAY2BGR)

    # 저화질 모드 적용
    if low_quality_mode:
        scale = 0.4  # 축소 비율 (값이 작을수록 더 픽셀화됨)
        small = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        frame = cv2.resize(small, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

        # 효과 적용한 것 녹화화
        small_out = cv2.resize(output_frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        output_frame = cv2.resize(small_out, (output_frame.shape[1], output_frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    # 녹화 중이면 영상 저장
    if recording:
        out.write(output_frame)  # 녹화된 프레임 저장

        #  녹화 표시 20프레임마다 깜빡이게
        blink_counter += 1
        if blink_counter // 20 % 2 == 0:
            cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)  # 빨간 점 (더 작게)

    else:
        # 녹화 중이 아닐 때 PREVIEW 표시
        cv2.putText(frame, 'PREVIEW', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 모드 정보 텍스트는 화면에만 표시
    if gray_mode:
        cv2.putText(frame, 'GRAY MODE', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    if low_quality_mode:
        cv2.putText(frame, 'LOW QUALITY MODE', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Camera Feed', frame)

    # 키 입력 처리
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 키
        break
    elif key == 32:  # Space
        if not recording:
            out = cv2.VideoWriter('old fashioned style video.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            recording = True
            blink_counter = 0  # 깜빡임 카운트트
        else:
            out.release()
            recording = False
    elif key == ord('g'):  # 'g' 키 흑백 모드 토글
        gray_mode = not gray_mode
        print(f"Gray mode toggled: {'ON' if gray_mode else 'OFF'}")
    elif key == ord('l'):  # 'l' 키 저화질 모드 토글
        low_quality_mode = not low_quality_mode
        print(f"Low quality mode toggled: {'ON' if low_quality_mode else 'OFF'}")

# 자원 해제
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

