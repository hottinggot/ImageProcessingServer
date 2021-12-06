# ImageProcessingServer

#### 3D 가구 배치 시뮬레이터에서 도면 이미지 처리를 수행하는 서버
OpenCV를 이용하여 도면 이미지의 3D 모델링을 위한 데이터를 추출한다.  

#### GrayScale 로 입력된 도면 이미지
![image](https://user-images.githubusercontent.com/59634669/144871541-808df15a-9403-4e54-a8e6-ae92aa4e738e.png)


#### Threshold
![image](https://user-images.githubusercontent.com/59634669/144871565-bd1060e7-63f0-4369-a695-73ef83b1dca5.png)


#### Morpology
직사각형으로 erosion 및 dilation을 여러 번 반복한다.  
![image](https://user-images.githubusercontent.com/59634669/144871602-7092fec1-9f77-4eff-8f4b-086ca63052d5.png)  
![image](https://user-images.githubusercontent.com/59634669/144871635-e6a56c5e-d191-40eb-a0af-f8cdb028fe96.png)


#### Contour
위의 방법으로 내벽의 좌표도 알아내고, 외벽과 내벽의 데이터를 이용하여 최종적으로 벽면 Object의 좌표를 추출한다.  
![image](https://user-images.githubusercontent.com/59634669/144872027-6af27a95-09b3-451b-826a-0dde57c37a07.png)  
![image](https://user-images.githubusercontent.com/59634669/144872037-ff009e3d-0a93-48d0-8a4a-8e715dd78d3c.png)

내부 공간을 추출한다.  
![image](https://user-images.githubusercontent.com/59634669/144872255-87f74d9b-4818-45de-9a54-e13bfa1d68e4.png)  
![image](https://user-images.githubusercontent.com/59634669/144872266-d81e744e-8f19-485e-baf2-770f0f81387b.png)

