package knu.cse.zzizzh.myapplication.PhysicalArchitecture;

import android.util.Base64;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Serializable;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Arrays;

public class Client extends Thread implements Serializable
{
    private Socket socket;
    private InetSocketAddress serverAddr;

    private clientWrite clientW;
    private clientRead clientR;

	private ClientControl cControl;

    char[] buf;

    private static final String host = "125.137.84.142";
    private static final int port = 11117;

	private static Client client = null;

	public void run(){
        cControl = cControl.getcControl();
        socket = new Socket();
        serverAddr = new InetSocketAddress(host, port);

        try{
            socket.connect(serverAddr, 1000);
            Log.d("test11", "connect complete");
        }catch(Exception e){
            Log.d("test11", "connect fail");
            e.printStackTrace();
        }

        clientW=new clientWrite(socket);
        clientR=new clientRead(socket, cControl);

        if(socket.isConnected())
            Log.d("test11", "sock is connected");
        clientW.start();
        clientR.start();
    }

	static public Client getClient(){
		return client;
	}
	public ClientControl getcControl() {
		return cControl;
	}
	public void setcControl(ClientControl cControl) {
		this.cControl = cControl;
	}

	public void sendToServer(Object obj){
	    clientW.sendToServer(obj);
	    clientW.start();
    }
}

class clientRead extends Thread
{
    private Socket socket;
    private ClientControl clientControl;
    private BufferedReader in;
    private PrintWriter out;

    private char[] buf;
    private int len;
    private String result = null;

	public clientRead(Socket socket, ClientControl cControl)
	{
        buf = new char[1024*10];

		this.socket = socket;
		this.clientControl = cControl;
	}

    @Override
    public void run() {
        try{
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            //out=new PrintWriter(socket.getOutputStream(), true);
        }catch(IOException ie){
            ie.printStackTrace();
        }

	    while(true) {
	        result = "";
            len = 0;

            try {
                Thread.sleep(200);
                Log.d("test22", "receive wait..");

                while((len = in.read(buf, 0, 1024)) == 1024){
                    buf[1024] = '\0';
                    result += String.copyValueOf(buf);
                    Arrays.fill(buf, '\0');
                }

                buf[len] = '\0';
                result += String.copyValueOf(buf, 0, len+1);
                Arrays.fill(buf, '\0');

                Log.d("test22", "result length : " + result.length());
                clientControl.handleMeg(result);
            } catch (Exception e) {
                Log.d("test22", "data receive fail : " + result.length());
                e.printStackTrace();
            } finally {

            }
        }
    }

    private byte[] concatenate(byte[] a, byte[] b, int bLen) {
	    Log.d("test33", "in concat func");
        int aLen = a.length;

        byte[] c = new byte[aLen + bLen];
        System.arraycopy(a, 0, c, 0, aLen);
        System.arraycopy(b, 0, c, aLen, bLen);

        return c;
    }
}

class clientWrite extends Thread
{
	private Socket socket;

	private String console = "";
	private char[] buf;

	private PrintWriter out;

	private boolean sendToReadyString;
	private boolean sendToReadyChar;

	public clientWrite(Socket socket)
	{
		this.socket=socket;
		sendToReadyString=false;
        sendToReadyChar=false;

        try{
            out=new PrintWriter(socket.getOutputStream(), true);
        }catch(IOException ie){
            ie.printStackTrace();
        }

    }

    @Override
    public void run() {
		String temp = "#fin";
		//buf = new byte[1024];
	    buf = temp.toCharArray();

        while (sendToReadyString == true) {
            try {
                out.println((Base64.encode(temp.getBytes(), Base64.NO_WRAP)));
                Log.d("test11", "send to server complete");
            }catch(Exception e){
                e.printStackTrace();
                Log.d("test11", "send to server fail");
            }
            sendToReadyString = false;
        }
        while (sendToReadyChar == true) {
            try {
                //out.println(buf);
                //out.print(buf);
            }catch(Exception e){
                e.printStackTrace();
            }
            Log.d("test11", "send to server complete");

            sendToReadyChar = false;
        }

    }

    public void sendToServer(Object msg){

	    if(msg instanceof String) {
            sendToReadyString = true;
            console = (String)msg;
        }

        this.run();

	}

}
