public class Consumidor implements Runnable {
    // Atributos
    public int delay;
    public Deposito dep;
    public Thread t;

    // Métodos
    public Consumidor(Deposito dep, int delay) {
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
                for(int i = 0; i < 20; i++) {
                    if(dep.getNumItens() == 0) {
                        t.notify();
                        t.wait();
                    }

                    System.out.println("Consumindo produto de Nº " + dep.getNumItens() + "...");
                    dep.retirar();

                    t.sleep(delay);
                }
            }
        } catch(InterruptedException e) {
            System.out.println("Interrompendo Thread...");
        }
    }
}
