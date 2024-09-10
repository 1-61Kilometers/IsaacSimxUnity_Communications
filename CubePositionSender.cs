using UnityEngine;
using System.Net.Sockets;
using System.Text;
using Newtonsoft.Json;

public class CubePositionSender : MonoBehaviour
{
    private const string UDP_IP = "127.0.0.1";
    private const int UDP_PORT = 5005;

    private UdpClient udpClient;
    private Vector3 lastSentPosition;

    [SerializeField]
    private float sendInterval = 0.1f; // Send position every 0.1 seconds
    private float timer;

    private void Start()
    {
        udpClient = new UdpClient();
        lastSentPosition = transform.position;
    }

    private void Update()
    {
        timer += Time.deltaTime;

        if (timer >= sendInterval)
        {
            timer = 0f;
            Vector3 currentPosition = transform.position;

            if (currentPosition != lastSentPosition)
            {
                SendPosition(currentPosition);
                lastSentPosition = currentPosition;
            }
        }
    }

    private void SendPosition(Vector3 position)
    {
        float[] positionArray = new float[] { position.x, position.y, position.z };
        string jsonMessage = JsonConvert.SerializeObject(positionArray);
        byte[] data = Encoding.UTF8.GetBytes(jsonMessage);
        udpClient.Send(data, data.Length, UDP_IP, UDP_PORT);
        Debug.Log($"Sent position: {jsonMessage}");
    }

    private void OnApplicationQuit()
    {
        if (udpClient != null)
        {
            udpClient.Close();
        }
    }
}