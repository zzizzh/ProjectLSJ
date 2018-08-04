package knu.cse.zzizzh.myapplication.Activity;

import android.content.Context;
import android.graphics.Bitmap;
import android.net.wifi.WifiManager;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import knu.cse.zzizzh.myapplication.Constants.Constant;
import knu.cse.zzizzh.myapplication.PhysicalArchitecture.Client;
import knu.cse.zzizzh.myapplication.PhysicalArchitecture.ClientControl;
import knu.cse.zzizzh.myapplication.R;

public class MainActivity extends AppCompatActivity {
    private ClientControl clientControl;

    private ImageView imageView;
    private TextView textView;
    private static MainActivity mainActivity;

    private Handler imageHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d("PROJ", "MainActivity");

        mainActivity = this;
        clientControl = ClientControl.getcControl();
        clientControl.getClient().start();

        imageView = findViewById(R.id.imageView);

        imageHandler = new Handler(){
            @Override
            public void handleMessage(Message msg) {
                if(msg.what == Constant.MessageType.STREAMING.getType()){
                    if(msg.obj != null) {
                        if(msg.obj instanceof Bitmap) {
                            Log.d("test11", "bitmap image received complete");
                            imageView.setImageBitmap((Bitmap) msg.obj);
                            //imageView.refreshDrawableState();
                        }
                        else{
                            Log.d("test11", "bitmap image received fail");
                        }
                    }
                }
                else if(msg.what == Constant.MessageType.ALARM.getType()){
                    textView.setText((String)msg.obj);
                }
                else{
                    Log.d("test11", "handler get unexpected msg type");
                }
                //TODO 기능 추가 시 else if문으루다가
            }
        };
        clientControl.setImageHandler(imageHandler);
    }

    public ImageView getImageView(){
        return imageView;
    }

    public TextView getTextView() {
        return textView;
    }
}
