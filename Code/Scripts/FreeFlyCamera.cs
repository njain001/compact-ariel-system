using UnityEngine;

/**
 * @file FreeFlyCamera.cs
 * @brief Controls for a free-flying camera in Unity.
 *
 * This script allows for a 3D camera in Unity to be moved freely in space
 * using mouse and keyboard input, typically for debugging or navigating 3D environments.
 */

public class FreeFlyCamera : MonoBehaviour
{
    /** @brief Speed of camera movement. */
    public float speed = 10.0f;

    /** @brief Sensitivity of mouse movement. */
    public float sensitivity = 0.5f;

    /** 
     * @brief Last mouse position vector.
     *
     * Stores the position of the mouse in the last frame,
     * used for calculating movement in the current frame.
     */
    private Vector3 lastMousePosition = new Vector3(255, 255, 255);

    /**
     * @brief Update is called once per frame.
     *
     * Handles user input for moving the camera.
     */
    void Update()
    {
        // Check if the Shift key is pressed to enable camera movement
        if (Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.RightShift))
        {
            // Calculate the mouse movement difference from the last frame
            lastMousePosition = Input.mousePosition - lastMousePosition;
            // Adjust the camera's rotation based on the mouse movement
            lastMousePosition = new Vector3(-lastMousePosition.y * sensitivity, lastMousePosition.x * sensitivity, 0);
            // Update the camera's rotation
            lastMousePosition = new Vector3(transform.eulerAngles.x + lastMousePosition.x, transform.eulerAngles.y + lastMousePosition.y, 0);
            transform.eulerAngles = lastMousePosition;
            // Store the new last mouse position
            lastMousePosition = Input.mousePosition;

            // Initialize a direction vector for movement
            Vector3 direction = new Vector3();
            
            // Process keyboard inputs to determine the direction
            direction += Input.GetKey(KeyCode.W) ? transform.forward : Vector3.zero;
            direction += Input.GetKey(KeyCode.S) ? -transform.forward : Vector3.zero;
            direction += Input.GetKey(KeyCode.A) ? -transform.right : Vector3.zero;
            direction += Input.GetKey(KeyCode.D) ? transform.right : Vector3.zero;
            direction += Input.GetKey(KeyCode.E) ? transform.up : Vector3.zero;
            direction += Input.GetKey(KeyCode.Q) ? -transform.up : Vector3.zero;

            // Move the camera position based on input, speed, and the time since the last frame
            transform.position += direction * speed * Time.deltaTime;
        }
    }
}
