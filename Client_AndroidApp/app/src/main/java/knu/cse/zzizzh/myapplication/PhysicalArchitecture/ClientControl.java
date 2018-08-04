package knu.cse.zzizzh.myapplication.PhysicalArchitecture;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Handler;
import android.os.Message;
import android.util.Base64;
import android.util.Log;

import knu.cse.zzizzh.myapplication.Constants.Constant;

public class ClientControl {
	private String reply = "";
    private Client client;

    private Handler imageHandler = null;
	private Handler messageHandler = null;

	/*
		checking request complete
	 */
	private boolean login = false;
	private long startTime = 0;

    private static ClientControl cControl = new ClientControl();

    public ClientControl() {
        client = new Client();
    }

    public static ClientControl getcControl(){
        return cControl;
    }

	/*
		received data control
	 */
	public void handleMeg(String imageString){
		Log.d("test11", "in handleMsg");
		Log.d("test11","message length in handleMeg : " + imageString.length());

		streaming(imageString);

		// TODO 기능추가하면 여기서 메시지 핸들링
	}

	public void login(String id, String pass){
		if(!login) {
			startTime = System.currentTimeMillis();

			login = true;

			reply = "#login%";
			reply += id;
			reply += "%";
			reply += pass;

			client.sendToServer(reply);

			reply = "";
		}
	}

	public void streaming(String imageString){
		reply = "#fin%image";

		Bitmap data = getImageFromString(imageString);

		if(data == null)
			Log.d("test11", "fail decode bitmap");

		Message message = new Message();
		message.what = Constant.MessageType.STREAMING.getType();
		message.obj = data;

		imageHandler.sendMessage(message);

		client.sendToServer(reply);
		Log.d("test11", "end streaming func");
	}

	public void printMessage(String msg){
		reply = "#fin%message";

		Message message = new Message();
		message.what = Constant.MessageType.ALARM.getType();
		message.obj = (Object)msg;

		messageHandler.sendMessage(message);

		client.sendToServer(reply);
	}
	/*
		get and set method
	 */

	public Client getClient(){
		return client;
	}

	public boolean isLogin() {
		return login;
	}

	public long getStartTime() {
		return startTime;
	}

	public void setLogin(boolean login) {
		this.login = login;
	}


    public Bitmap getImageFromString (String imageString){

		Bitmap decodedBitmap = null;
		try {
			byte[] decodedByteArray = Base64.decode(imageString.getBytes(), Base64.NO_WRAP);
			decodedBitmap = BitmapFactory.decodeByteArray(decodedByteArray, 0, decodedByteArray.length);
		}catch(Exception e){
			e.printStackTrace();
			Log.d("test44", "bitmap decode fail");
			decodedBitmap = null;
		}finally {
			return decodedBitmap;
		}
    }

    public void setImageHandler(Handler imageHandler){
		this.imageHandler = imageHandler;
	}

	public void setmessageHandler(Handler messageHandler){
		this.messageHandler = messageHandler;
	}
}
