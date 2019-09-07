package com.minho.zapgram.client;

import com.minho.zapgram.server.ServerInterface;

import javax.swing.*;
import javax.swing.border.*;
import javax.swing.text.*;

import java.awt.*;
import java.awt.event.*;
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.util.*;

public class ChatUI{
    /** ATTRIBUTES **/
    // Chat Objects
    private ChatClient client;
    private ServerInterface server;

    // GUI Objects
    private JFrame frame;
    private JTextPane chatText;
    private JTextField msgField, ipField, portField, nickField;
    private JButton connectBt, sendBt;
    private JList peersLst;

    /** METHODS **/
    // Class Constructor
    public ChatUI() {
        // Initializing the Window and Component Panels
        frame = new JFrame("Zapgram Chat - Cliente");
        JPanel main = new JPanel();
        JPanel top = new JPanel();
        JPanel chat = new JPanel();
        JPanel bottom = new JPanel();

        // Initializing the GUI Components
        ipField = new JTextField();
        portField = new JTextField();
        msgField = new JTextField();
        nickField = new JTextField();
        chatText = new JTextPane();
        connectBt = new JButton("Conectar");
        sendBt = new JButton("Enviar");
        peersLst = new JList();

        // Initializing the Scrolling Panels
        JScrollPane chatScroll = new JScrollPane(chatText);
        JScrollPane peersScroll = new JScrollPane(peersLst);

        // Configuring the Frame properties
        frame.setSize(800,600);
        frame.setContentPane(main);
        frame.setResizable(false);
        frame.setVisible(true);
        frame.setLocationRelativeTo(null);

        // Configuring the Panel layouts
        main.setLayout(new BorderLayout(5,5));
        top.setLayout(new GridLayout(1,7,5,5));
        chat.setLayout(new BorderLayout(5,5));
        bottom.setLayout(new BorderLayout(5,5));

        peersScroll.setPreferredSize(new Dimension(150,0));

        main.setBorder(new EmptyBorder(10, 10, 10, 10) );

        // Configuring the components properties
        chatText.setEditable(false);
        msgField.setEditable(false);

        // Linking Components to desired Panels
        top.add(new JLabel("Nickname: ", SwingConstants.RIGHT)); top.add(nickField);
        top.add(new JLabel("Chat IP: ", SwingConstants.RIGHT)); top.add(ipField);
        top.add(new JLabel("Chat Port: ", SwingConstants.RIGHT)); top.add(portField);
        top.add(connectBt);

        chat.add(chatScroll, BorderLayout.CENTER);
        chat.add(peersScroll, BorderLayout.EAST);

        bottom.add(msgField, BorderLayout.CENTER);
        bottom.add(sendBt, BorderLayout.EAST);

        main.add(top, BorderLayout.NORTH);
        main.add(chat, BorderLayout.CENTER);
        main.add(bottom, BorderLayout.SOUTH);

        // COMPONENTS EVENT HANDLING
        frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                if(connectBt.getText().equals("Desconectar")) {
                    try {
                        server.logout(client);
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

        nickField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });

        ipField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });

        portField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { doConnect(); }
        });

        sendBt.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { sendText(); }
        });

        msgField.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) { sendText(); }
        });


    }

    // Method for Creating a Remote Connection with the Server
    public void doConnect() {
        if (connectBt.getText().equals("Conectar")) {
            if (nickField.getText().length() < 2) {
                JOptionPane.showMessageDialog(frame, "Digite um Nickname para entrar no Chat!",
                                            "Atenção!", JOptionPane.WARNING_MESSAGE);
                return;
            }

            if (ipField.getText().length() < 2 || portField.getText().length() < 2) {
                JOptionPane.showMessageDialog(frame, "Digite o IP e Porta onde o Servidor do Chat está conectado!",
                                            "Atenção!", JOptionPane.WARNING_MESSAGE);
                return;
            }

            try {
                client = new ChatClient(nickField.getText(), this);

                server = (ServerInterface) Naming.lookup("rmi://" + ipField.getText() + ":" + portField.getText() + "/zapgram");

                for(Object peer: server.getConnected()) {
                    if (((ClientInterface) peer).getName().equals(nickField.getText())) {
                        JOptionPane.showMessageDialog(frame, "Já há alguém com este Nickname!\nEscolha outro.",
                                "Atenção!", JOptionPane.WARNING_MESSAGE);
                        return;
                    }
                }

                server.login(client);
                updateUsers(server.getConnected());

                connectBt.setText("Desconectar");

                nickField.setEditable(false);
                ipField.setEditable(false);
                portField.setEditable(false);
                msgField.setEditable(true);

            } catch(Exception e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
            }
        } else {
            try {
                server.logout(client);

                updateUsers(null);

                msgField.setText("");
                chatText.setText("");

                connectBt.setText("Conectar");
                nickField.setEditable(true);
                ipField.setEditable(true);
                portField.setEditable(true);
                msgField.setEditable(false);

            } catch(Exception e) {
                e.printStackTrace();
                JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    // Method to Send a Message to be Forwarded by the Server
    public void sendText() {
        if (connectBt.getText().equals("Conectar")){
            JOptionPane.showMessageDialog(frame, "Você precisa estar conectado para enviar mensagens!",
                                      "Atenção!", JOptionPane.WARNING_MESSAGE);
            return;
        }

        try {
            if(msgField.getText().length() > 0) {
                server.deliver("[" + nickField.getText() + "]: " + msgField.getText());
                msgField.setText("");
            }
        } catch(Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
        }
    }

    // Method to Print a Message in the Chat text box
    public void writeMsg(String st) {

        try {
            StyleContext sc = StyleContext.getDefaultStyleContext();
            AttributeSet aset;

            if (st.matches("(^\\[System\\].*)|(^MSG #.*\\[System\\].*)")) {
                updateUsers(server.getConnected());
                aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, Color.RED);
            }
            else if (st.matches("(^\\[" + nickField.getText() + "\\].*)|(^MSG #.*\\[" + nickField.getText() + "\\].*)"))
                aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, Color.BLUE);
            else
                aset = sc.addAttribute(SimpleAttributeSet.EMPTY, StyleConstants.Foreground, Color.DARK_GRAY);

            aset = sc.addAttribute(aset, StyleConstants.FontFamily, "Lucida Console");

            chatText.getStyledDocument().insertString(chatText.getDocument().getLength(), st+'\n', aset);

        }
        catch (RemoteException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(frame, "Falha de Conexão", "Erro!", JOptionPane.ERROR_MESSAGE);
        }
        catch (BadLocationException exp) { exp.printStackTrace(); }
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

    // Main Function
    public static void main(String [] args) {
        ChatUI c = new ChatUI();
    }

}