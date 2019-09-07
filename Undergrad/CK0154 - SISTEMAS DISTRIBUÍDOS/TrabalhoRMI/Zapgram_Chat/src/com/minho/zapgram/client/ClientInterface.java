package com.minho.zapgram.client;

import java.rmi.*;

public interface ClientInterface extends Remote {
    public void post(String msg) throws RemoteException;
    public String getName() throws RemoteException;
}
