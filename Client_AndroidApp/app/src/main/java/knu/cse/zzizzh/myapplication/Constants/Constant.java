package knu.cse.zzizzh.myapplication.Constants;

public class Constant {

    public enum MessageType {
        STREAMING(0), ALARM(1);

        private int type;

        MessageType(int type){
            this.type = type;
        }

        public int getType() {
            return type;
        }
    }
}
