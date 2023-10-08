import pydicom
import os
import numpy as np
import nibabel
import skimage.measure as measure
from pydicom.uid import ExplicitVRLittleEndian
import tkinter
from tkinter import filedialog
import warnings
warnings.filterwarnings("ignore")


#Function to get the maximum contour region, by default this has to be the body mask
def get_max(props):
    area=0
    k=0
    #Find max area contour to get the largest contour
    for idx,p in enumerate(props):
        if p.area>area:
            area=p.area
            k=idx
    return k

def maybedir(path):
	if not os.path.exists(path):
		os.mkdir(path)

#####################
#Reading Dicom Images
#####################
root = tkinter.Tk()
root.withdraw()

currdir = os.getcwd()
PathDicom = filedialog.askdirectory(parent=root, initialdir=currdir, title='C:\\Users\\juliu\\Documents\\dicomimage\\test_wb_ct\\ScalarVolume_9')
if len(PathDicom) > 0:
    print(('You chose %s')%PathDicom)
dicom_output_folder = 'dicom_files' #Path to store the nifti file after getting new segmentations
nifti_output_folder = 'nifti_files' #Path to store the dicom files after getting new segmentations
patient_height = float(input("Enter Patient's Height: "))
#Iterate through the dicom files
lstFilesDCM = []
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if '.dcm' in filename.lower():
            lstFilesDCM.append(os.path.join(dirName,filename))

#Read the header of the first dicom file to get the details
RefDs = pydicom.dcmread(lstFilesDCM[3])
RefDs_2 = pydicom.dcmread(lstFilesDCM[4])

ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))    
cal = RefDs.RescaleIntercept

ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

for i in lstFilesDCM:
    ds = pydicom.dcmread(i)
    
    ArrayDicom[:, :, lstFilesDCM.index(i)] = ds.pixel_array
#####################
#Creating Body Masks#
#####################
#Convert the array pixels to HU values using the rescale and intercept values from the header
ArrayDicom = ArrayDicom*int(RefDs.RescaleSlope)+cal    
binary_Mask = ArrayDicom >-500

#Threshold and apply conotur to get only max contour region

a = measure.label(binary_Mask)
props = measure.regionprops(a)
#Find the max contour index
k=get_max(props)
temp_arr = np.zeros(binary_Mask.shape)
#Store the max contour region in an empty array
temp_arr[a == props[k].label] = binary_Mask[a == props[k].label].flatten()[0]
#This will store the binary mask of the body region

#Mutliply the thresholded region with the new mask
new_arr = temp_arr*ArrayDicom
#Make zeros to air HU values
new_arr[temp_arr==0]=-1024

##################################
#Finding Patient's Weight and BMI#
##################################

#Find all sum of ones
total_ones = np.sum(temp_arr)
slice_thickness = np.abs(float(RefDs.ImagePositionPatient[2]) - float(RefDs_2.ImagePositionPatient[2]))

#Store voxel spacings from header metadata using Pixel Spacing and Slice Thinckness information
aff = [float(RefDs.PixelSpacing[0]),float(RefDs.PixelSpacing[1]),slice_thickness]
#Get the voxel spacing values by multiplying with the product value of each voxel
voxel = np.prod(tuple(aff)) * 1e-9
patient_vol = total_ones * voxel

Pat_weight = patient_vol * (1000)

print(f"Patient's weight is {Pat_weight} kg")

patient_height_mm2 = (patient_height/100)*(patient_height/100) #Convert height to mm2

bmi = Pat_weight/patient_height_mm2 

print(f"Patient's BMI is {bmi}")

if(bmi>0): # This condition determines the users bmi greater than zero
    if(bmi<=18.5): # This condition determines if the user's bmi is within the catergory less than or equal to 18.5 and prompt user of the status 
        print("\nThis is considered to be underweight")
    elif(bmi<=25): # This condition determines if the user's bmi is within the catergory less than or equal to 25 and prompt user of the status
        print("\nThis is considered to be normal")
    elif(bmi<=30): # This condition determines if the user's bmi is within the catergory less than or equal to 30 and prompt user of the status
        print("\nThis is considered to be overweight")
    else: 
        print("\nThis is considered to be obese") # Prompt user of there bmi status if greater than 30
else:
    print("enter valid details") # prompt user to enter correct variable type to avoid error

####################################
#Saving the modified Image and Mask#
####################################

# #store voxel spacings as affine to save as nifti file from voxel spacings obtained earlier
# new_affine = np.eye(4)
# new_affine[0][0] = aff[0]
# new_affine[1][1] = aff[1]
# new_affine[2][2] = aff[2]

# #Store the file as a nifti file
# if nifti_output_folder!='na':
#     nifti_output_folder = nifti_output_folder
#     maybedir(nifti_output_folder)
#     nibabel.save(nibabel.Nifti1Image(new_arr.astype('int16'),new_affine),f'{nifti_output_folder}/img.nii.gz')
#     nibabel.save(nibabel.Nifti1Image(temp_arr.astype('int16'),new_affine),f'{nifti_output_folder}/mask.nii.gz')

# #Convert the HU values back to pixel array while saving as a dicom file
# new_arr = ((new_arr.astype('int16')-int(cal))/int(RefDs.RescaleSlope)).astype('int16')
# if dicom_output_folder!='na':
#     dicom_output_folder  = dicom_output_folder
#     maybedir(dicom_output_folder)
#     #Iterate through each dicom file and save the new pixel array values
#     for idx,path in enumerate(lstFilesDCM):
#         filename = path.split('\\')[-1]
#         img = pydicom.dcmread(path)
#         img.PixelData = new_arr[...,idx].astype('int16').tobytes()
        
#         img.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
#         img.save_as(f'{dicom_output_folder}/{filename}')
