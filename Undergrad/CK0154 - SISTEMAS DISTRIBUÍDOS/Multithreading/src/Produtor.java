public class Produtor implements Runnable {
    // Atributos
    public int delay;
    public Deposito dep;
    public Thread t;

    // Métodos
    public Produtor(Deposito dep, int delay) {
        this.dep = dep;
        this.delay = delay;
    }

    public void start() {
        if(t == null) {
            t = new Thread(this);
            t.start();
        }
    }

    public void run() {
        try {
            synchronized (this){
                for(int i = 0; i < 100; i++) {
                    if(dep.getNumItens() == 10) {
                        t.notify();
                        t.wait();
                    }

                    System.out.println("Produzindo o produto de Nº " + dep.getNumItens() + "...");
                    dep.colocar();

                    t.sleep(delay);
                }
            }
        } catch(InterruptedException e) {
            System.out.println("Interrompendo Thread...");
        }
    }
}

public class RacerThread extends Thread {
    // Atributos
    private String name;

    // Métodos
    public RacerThread(String name, int priority){
        super();
        this.name = name;
        this.setPriority(priority);
    }

    public void correr() {
        try {
            for (int i = 0; i < 1000; i++) {
                System.out.println("Corredor " + this.name + " correndo.");
                sleep(100);
            }
        } catch (InterruptedException e) {
            System.out.println("Interrupted");
        }

    }

    @Override
    public void run() {
        this.correr();
    }
}