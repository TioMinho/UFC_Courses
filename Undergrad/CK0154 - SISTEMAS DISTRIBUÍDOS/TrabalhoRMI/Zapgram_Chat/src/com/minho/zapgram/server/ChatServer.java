package com.minho.zapgram.server;

import com.minho.zapgram.client.ClientInterface;

import java.rmi.*;
import java.rmi.server.*;
import java.util.Vector;

public class ChatServer extends UnicastRemoteObject implements ServerInterface {
    /** ATTRIBUTES **/
    private Vector peers;
    private int msgCounter;
    private ServerUI ui;

    /** METHODS **/
    public ChatServer(ServerUI ui) throws RemoteException {
        super();

        this.peers = new Vector();
        this.msgCounter = 0;
        this.ui = ui;
    }

    @Override
    public boolean login(ClientInterface cli) throws RemoteException {
        System.out.println("[System] " + "Conectando " + cli.getName() + " ...");

        peers.add(cli);
        ui.updateUsers(peers);

        cli.post("[System] Você está conectado no Zapgram Chat!");
        deliver("[System] " + cli.getName() + " acabou de entrar.");

        return true;
    }

    @Override
    public boolean logout(ClientInterface cli) throws RemoteException {
        System.out.println("[System] " + "Desconectando " + cli.getName() + " ...");

        deliver("[System] " + cli.getName() + " acabou de sair.");

        peers.remove(cli);
        ui.updateUsers(peers);

        return true;
    }

    @Override
    public void deliver(String msg) throws RemoteException {
        System.out.println(msg);

        msgCounter++;

        for (Object peer: peers) {
            try {
                ClientInterface cli = (ClientInterface) peer;
                cli.post("MSG #" + msgCounter + " - " + msg);
            } catch(RemoteException e) {
                // Cliente Não Está Respondendo
            }
        }

        ui.writeMsg("MSG #" + msgCounter + " - " + msg);
    }

    @Override
    public Vector getConnected() throws RemoteException {
        return peers;
    }

    public void cleanServer() throws RemoteException {
        while(!peers.isEmpty()) logout((ClientInterface) peers.firstElement());
    }

}
