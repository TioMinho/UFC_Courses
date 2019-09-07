package com.minho.zapgram.server;

import com.minho.zapgram.client.ClientInterface;
import java.rmi.*;
import java.util.Vector;

public interface ServerInterface extends Remote {
    public boolean login(ClientInterface cli) throws RemoteException;
    public boolean logout(ClientInterface cli) throws RemoteException;
    public void deliver(String msg) throws RemoteException;
    public Vector getConnected() throws RemoteException;
}
