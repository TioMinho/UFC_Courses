package com.minho.zapgram.client;

import java.rmi.*;
import java.rmi.server.UnicastRemoteObject;

public class ChatClient extends UnicastRemoteObject implements ClientInterface {
    /** ATTRIBUTES **/
    private String nickname;
    private ChatUI ui;

    /** MEHTODS **/
    public ChatClient(String nickname, ChatUI ui) throws RemoteException {
        this.nickname = nickname;
        this.ui = ui;
    }

    @Override
    public void post(String msg) {
        System.out.println(msg);
        ui.writeMsg(msg);
    }

    @Override
    public String getName() {
        return nickname;
    }

}
