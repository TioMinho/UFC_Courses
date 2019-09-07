package com.minho.zapgram.server;

import com.minho.zapgram.client.ChatClient;
import com.minho.zapgram.client.ClientInterface;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.ExportException;
import java.util.Vector;
import javax.swing.*;
import javax.swing.border.*;
import javax.swing.text.*;

import java.awt.*;
import java.awt.event.*;
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.util.*;

public class ServerUI {
    /** ATTRIBUTES **/
    // Chat Objects
    private ServerInterface server;

    // GUI Objects
    private JFrame frame;
    private JTextPane chatText;
    private JTextField ipField, portField;
    private JButton connectBt;
    private JList peersLst;
    private JLabel statusLb;

    /** METHODS **/
    // Class Constructor
    public ServerUI() {
        // Initializing the Window and Component Panels
        frame = new JFrame("Zapgram Chat - Servidor");
        JPanel main = new JPanel();
        JPanel top = new JPanel();
        JPanel chat = new JPanel();

        // Initializing the GUI Components
        ipField = new JTextField();
        portField = new JTextField();
        chatText = new JTextPane();
        connectBt = new JButton("Conectar");
        peersLst = new JList();
        statusLb = new JLabel("Offline");

        // Initializing the Scrolling Panels
        JScrollPane chatScroll = new JScrollPane(chatText);
        JScrollPane peersScroll = new JScrollPane(peersLst);

        // Configuring the Frame properties
        frame.setSize(600,400);
        frame.setContentPane(main);
        frame.setResizable(false);
        frame.setVisible(true);
        frame.setLocationRelativeTo(null);

        // Configuring the Panel layouts
        main.setLayout(new BorderLayout(5,5));
        top.setLayout(new GridLayout(1,0,5,5));
        chat.setLayout(new BorderLayout(5,5));

        peersScroll.setPreferredSize(new Dimension(150,0));

        main.setBorder(new EmptyBorder(10, 10, 10, 10) );

        // Configuring the components properties
        chatText.setEditable(false);
        statusLb.setForeground(Color.RED);

        // Linking Components to desired Panels
        top.add(statusLb);
        top.add(new JLabel("IP: ", SwingConstants.RIGHT)); top.add(ipField);
        top.add(new JLabel("Port: ", SwingConstants.RIGHT)); top.add(portField);
        top.add(connectBt);

        chat.add(chatScroll, BorderLayout.CENTER);
        chat.add(peersScroll, BorderLayout.EAST);

        main.add(top, BorderLayout.NORTH);
        main.add(chat, BorderLayout.CENTER);

        // COMPONENTS EVENT HANDLING
        frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                if(connectBt.getText().equals("Desconectar")) {
                    try {
                        server.deliver("[System] Atenção! O servidor o Zapgram Chat irá se desligar em 3 segundos...");
                        Thread.sleep(3000);

                        int numPeers = server.getConnected().size();
                        for(int i = 0; i < numPeers; i++)
                            server.logout((ClientInterface) server.getConnected().firstElement());


                        Naming.unbind("rmi://" + ipField.getText() + ":" + portField.getText() + "/zapgram");
                    }
                    catch(Exception excp) {
                        excp.printStackTrace();
                        JOptionPane.showMessageDialog(frame, "Falha de Conexão",
                                "Erro!", JOptionPane.ERROR_MESSAGE);
                    }
                }

                super.windowClosing(e);
                System.exit(0);
            }
        });

        connectBt.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });

        ipField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });

        portField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });
    }

    // Method for Connecting the Server to the Specified IP and Port
    public void doConnect() {
        if (connectBt.getText().equals("Conectar")) {
            if (ipField.getText().length() < 2 || portField.getText().length() < 2) {
                JOptionPane.showMessageDialog(frame, "Digite o IP e Porta onde o Servidor deverá estar conectado!",
                        "Atenção!", JOptionPane.WARNING_MESSAGE);
                return;
            }

            try {
                try {
                    LocateRegistry.createRegistry(Integer.parseInt(portField.getText()));
                } catch(ExportException e) { }

                server = new ChatServer(this);
                Naming.rebind("rmi://" + ipField.getText() + ":" + portField.getText() + "/zapgram", server);

                connectBt.setText("Desconectar");

                ipField.setEditable(false);
                portField.setEditable(false);

                statusLb.setText("Online"); statusLb.setForeground(Color.GREEN);

                server.deliver("[System] O Zapgram Chat está online!");

            } catch(Exception e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
            }
        } else {
            try {
                server.deliver("[System] Atenção! O servidor o Zapgram Chat irá se desligar em 3 segundos...");
                Thread.sleep(3000);

                int numPeers = server.getConnected().size();
                for(int i = 0; i < numPeers; i++)
                    server.logout((ClientInterface) server.getConnected().firstElement());


                System.out.println("TESTE");
                Naming.unbind("rmi://" + ipField.getText() + ":" + portField.getText() + "/zapgram");

                chatText.setText("");
                updateUsers(null);
                connectBt.setText("Conectar");

                ipField.setEditable(true);
                portField.setEditable(true);

                statusLb.setText("Offline"); statusLb.setForeground(Color.RED);

            } catch(Exception e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    // Method to Update the List of Online Users
    public void updateUsers(Vector v){
        DefaultListModel listModel = new DefaultListModel();

        if(v != null) {
            for (Object peer : v) {
                try {
                    String tmp = ((ClientInterface) peer).getName();
                    listModel.addElement(tmp);
                } catch (Exception e) { e.printStackTrace(); }
            }
        }

        peersLst.setModel(listModel);
    }

    // Method to Print a Message in the Chat text box
    public void writeMsg(String st) {

        try {
            StyleContext sc = StyleContext.getDefaultStyleContext();
            AttributeSet aset;

            if (st.matches("(^\\[System\\].*)|(^MSG #.*\\[System\\].*)"))
                aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, Color.RED);
            else
                aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, Color.DARK_GRAY);

            aset = sc.addAttribute(aset, StyleConstants.FontFamily, "Lucida Console");

            chatText.getStyledDocument().insertString(chatText.getDocument().getLength(), st+'\n', aset);

        }
        catch (BadLocationException exp) { exp.printStackTrace(); }
    }

    public static void main(String[] args) {
        ServerUI ui = new ServerUI();
    }

}