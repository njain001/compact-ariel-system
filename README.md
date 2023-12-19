# compact-ariel-system
Create 3D model of building integrating room data such as temperature, humidity etc

# Taking videos and Photos for building a 3d model

-  We are required to create a game in Unity using a 3d model which we will be building in the Agisoft Metashape. The Model is built by taking videos and photos from a drone which was flown on the first Sunday of December 2023
-  We have automated the drone flight path using an application Drone Link, which enables a user to create or fix a path that a drone follows to take videos and photos
-  After taking the required photos and videos we need to process the videos to get the videos to be transformed into frames. 
-  After creating frames for the entire video that is taken by the drone we will be giving the set of frames that are required to build a 3d model to Agisoft Meta shape.

# Processing the 3d model to a finished product:

-  After creating  a 3d model, we will import the 3d model into the Blender to preprocess and fix any issues related to texture and color correction.
-  After doing the changes, we will save and export the model into a Unity.


# Working on Unity to Build the Game/ Digital Twin:
-  After doing the required refinements to the 3d model we import the 3d model which is .obj file onto a Unity game space.
-  The Unity namespace is a 3d space where we can create we need to drag the 3d model into the gamespace, where we will be scaling the model into your requirements.
-  After dragging and dropping the model into the 3d space we will need to create a few game objects.

# Creating game objects on the 3d model
-  The game objects are what will be used to make your model interactive to your inputs.
-  There are 3 game objects mainly that you are needed to create namely Directional lighting, Camera, UserInteractive Canvas InputField.
-  ## Directional Lighting:
    It is used to brighten the areas that you want. I have placed 3 Directional Lighting two at the front of the 3d model and one to the side of the building.
-  ## Camera:
   Camera is the one of the main components that is used to fix the point of view towards the building. The Camera needs to be placed accurately as we would be attaching c# code to it for moving around the 3d model. We will be adding facilities like zooming onto a 3d model, zooming out, moving right and left on the 3d model, moving up and down on the 3d model. It is important to note that we would be also using also using the mouse pointer to set the point of view.
- ## UI Input Text field:
  This is used to display the text that is obtained after getting making an API call onto the Google Sheets API to fetch the the last row data.It is displayed in the format that is mentioned in the Test1 c# code in the Scripts folder of the repository. It is also showing the the units with the data. The data which is fetched in the form of .JSON format is converted into a string and then it is displayed in the form of key object pair. Make sure to place the input TextField at the right place so that it does not hamper your view in the build.

# Using Scripts:
Scripts are generally used to add functionalities to the game objects . These scripts are written in c# code which is supported by the Unity. The scripts that are used in this project is mainly FreeFlyCamera which is used to add the functionality to the Camera and Test1 which is used to display the text onto the input TextField.


# Downloading Unity and Running the Build file:

-  For downloading the Unity onto your device please use this link https://unity.com/download, which will also download VS code if it is not installed before. After downloading the Unity it will ask to even download Unity Hub to create and manage different Unity Projects. After downloading Unity and UnityHub successfully, now create a New Unity Project and create sub folders like Assets. In the Assets folder create sub folders like Model and Scripts and import the files into the folders respectively. 
-  After setting and following all the steps above, now to is the time to build and run the game. Go to the menu and select Build Option. After selecting build, you will enter into a drop box with options. Select the option ”Build and Run” to save and run the game. If there are no errors the game will run and update the values which is received from the google sheets

