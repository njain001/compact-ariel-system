
using UnityEngine;

public class FreeFlyCamera : MonoBehaviour
{
    // Speed of camera movement
    public float speed = 10.0f;

    // Sensitivity of mouse movement
    public float sensitivity = 0.5f;

     // Store the last mouse position for calculating movement
    private Vector3 lastMousePosition = new Vector3(255, 255, 255);

    void Update()
    {
        // Check if the Shift key is pressed
        if (Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.RightShift))
        {
            // Handle mouse movement
            lastMousePosition = Input.mousePosition - lastMousePosition;
            lastMousePosition = new Vector3(-lastMousePosition.y * sensitivity, lastMousePosition.x * sensitivity, 0);
            lastMousePosition = new Vector3(transform.eulerAngles.x + lastMousePosition.x, transform.eulerAngles.y + lastMousePosition.y, 0);
            transform.eulerAngles = lastMousePosition;
            lastMousePosition = Input.mousePosition;

            // Keyboard commands for the camera movement
            Vector3 direction = new Vector3();
            // Forward and backward movement
            if (Input.GetKey(KeyCode.W))
            {
                direction += transform.forward;
            }
            if (Input.GetKey(KeyCode.S))
            {
                direction += -transform.forward;
            }
            // Left and right strafing
            if (Input.GetKey(KeyCode.A))
            {
                direction += -transform.right;
            }
            if (Input.GetKey(KeyCode.D))
            {
                direction += transform.right;
            }
            // Up and down movement
            if (Input.GetKey(KeyCode.E))
            {
                direction += transform.up;
            }
            if (Input.GetKey(KeyCode.Q))
            {
                direction += -transform.up;
            }

            // Move the camera position based on input and speed
            transform.position += direction * speed * Time.deltaTime;
        }
    }
}

