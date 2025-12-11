### Backpropagation

odvození adaptačního pravidla

## Topologie vícevrstvé sítě

Vícevrstvá neuronová síť je tvořena minimálně třemi vrstvami neuronů: vstupní, výstupní a alespoň jednou vnitřní vrstvou. Vždy mezi dvěma sousedními vrstvami se pak nachází tzv. úplné propojení neuronů, tedy každý neuron nižší vrstvy je spojen se všemi neurony vrstvy vyšší.

Bias odpovídá váhové hodnotě přiřazené spojení mezi daným neuronem a fiktivním neuronem, jehož aktivace je vždy 1.

![](_page_1_Picture_3.jpeg)

# Standardní metoda backpropagation

Adaptační algoritmus **zpětného šíření chyby**  (*backpropagation*).

### **Samotný algoritmus obsahuje tři etapy**:

- dopředné (*feedforward*) šíření vstupního signálu tréninkového vzoru
- zpětné šíření chyby
- aktualizace váhových hodnot na spojeních

## Adaptační algoritmus backpropagation

*Krok 0.* Váhové hodnoty a bias jsou inicializovány malými náhodnými čísly.

Přiřazení inicializační hodnoty koeficientu učení .

*Krok 1.* Dokud není splněna **podmínka ukončení výpočtu**, opakovat kroky (2 až 9).

### **Podmínka ukončení:**

pokud již nenastávají žádné změny váhových hodnot nebo pokud již bylo vykonáno maximálně definované množství váhových změn, stop; jinak, pokračovat.

### Feedforward:

Krok 3. Aktivovat vstupní neurony  $(X_i, i=1, ...n)$  $x_i = s_i$ .

Krok 4 Vypočítat vstupní hodnoty vnitřních neuronů:  $(Z_i, j=1,..., p)$ :

$$z_{-}in_{j} = v_{0j} + \sum_{i=1}^{n} x_{i}v_{ij}.$$

Stanovení výstupních hodnot vnitřních neuronů

$$z_{j} = f(z_{in_{j}}).$$

Krok 5 Stanovení skutečných výstupních hodnoty signálu neuronové sítě  $(Y_k, k=1, ..., m)$ :

$$y_{i}n_{k} = w_{0k} + \sum_{j=1}^{p} z_{j} w_{jk},$$
  
 $y_{k} = f(y_{i}n_{k}).$ 

#### Backpropagation:

Krok 6 Ke každému neuronu ve výstupní vrstvě  $(Y_k, k=1, ..., m) \text{ je přiřazena hodnota očekávaného}$  výstupu pro vstupní tréninkový vzor. Dále je vypočteno  $\delta_k = (t_k - y_k) f'(y_- i n_k), \text{ které je součástí váhové}$  korekce  $\Delta w_{jk} = \alpha \ \delta_k z_j$  i korekce biasu  $\Delta w_{0k} = \alpha \ \delta_k.$ 

Krok 7 Ke každému neuronu ve vnitřní vrstvě (Zj, j=1, ..., p) je přiřazena sumace jeho delta vstupů (tj. z neuronů, které se nacházejí v následující vrstvě),

 $\delta_{-}in_{j} = \sum_{k=1}^{m} \delta_{k}w_{jk}$ . Vynásobením získaných hodnot derivací jejich aktivační funkce obdržíme  $\delta_{j} = \delta_{-}in_{j}f'(z_{-}in_{j})$ , které je součástí váhové korekce  $\Delta v_{ij} = \alpha \delta_{j}x_{i}$  i korekce biasu  $\Delta v_{0j} = \alpha \delta_{j}$ .

#### Aktualizace vah a prahů:

Krok 8 Každý neuron ve výstupní vrstvě  $(Y_k, k=1, ..., m)$  aktualizuje na svých spojeních váhové hodnoty včetně svého biasu (j=0, ..., p):

$$W_{jk}(new) = W_{jk}(old) + \Delta W_{jk}$$
.

Každý neuron ve vnitřní vrstvě ( $Z_j$ , j=1, ..., p) aktualizuje na svých spojeních váhové hodnoty včetně svého biasu (i=0, ..., n):

$$v_{ij}(new) = v_{ij}(old) + \Delta v_{ij}.$$

#### Krok 9. Podmínka ukončení:

pokud již nenastávají žádné změny váhových hodnot nebo pokud již bylo vykonáno maximálně definované množství váhových změn, stop; jinak, pokračovat.

### Trénovací množina

$$T = \{[x_1, t_1], \dots, [x_p, t_p]\}$$

 $m{x_j} = \left(x_{1j}, \dots, x_{nj}\right)$  vstupní vektor j. vzoru  $m{t_j} = \left(t_{1j}, \dots, t_{mj}\right)$  výstupní vektor j. vzoru p počet vzorů trénovací množiny

# **Chyba neuronové sítě**

$$E = \frac{1}{2} \sum_{j=1}^{p} \sum_{i=1}^{m} (y_{ij} - t_{ij})^{2}$$

$$m{y_j} = \left(y_{1j}, ..., y_{mj}
ight)$$
 skutečný výstupní vektor j. vzoru $m{t_j} = \left(t_{1j}, ..., t_{mj}
ight)$  požadovaný výstupní vektor j. vzoru

## Přírůstky vah

$$\Delta w_i = -\alpha \frac{\partial E}{\partial w_i} + \mu \Delta w_i'$$

- $\alpha$  koeficient učení z intervalu (0,1)
- $\mu$  koeficient setrvačnosti momentum z intervalu  $\langle 0,1 \rangle$
- $\Delta w_i^{'}$  změna váhy v předchozím kroku

- $\bullet \quad \frac{\partial E}{\partial w_i} = \frac{\partial E}{\partial y} \cdot \frac{\partial y}{\partial y_i} \cdot \frac{\partial y_i}{\partial w_i}$
- $E = \frac{1}{2}(y_i t_i)^2$  chyba pro *i*. výstupní neuron
- $y = \frac{1}{1 + e^{-\lambda \cdot y_{-}in}} = \left(1 + e^{-\lambda \cdot y_{-}in}\right)^{-1}$  aktivační (přenosová) funkce logická sigmoida ( $\lambda$  je parametr strmost sigmoidy)
- $y_{-}in = \sum_{i} x_{i} \cdot w_{i}$  vnitřní potenciál neuronu .... jedna složka  $y_{-}in = x_{i} \cdot w_{i}$

### **Přírůstky vah mezi vnitřní a výstupní vrstvou:**

$$\frac{\partial E}{\partial w_i} = \frac{\partial E}{\partial y} \cdot \frac{\partial y}{\partial y_i in} \cdot \frac{\partial y_i in}{\partial w_i}$$

SKRIPTA:
$$\delta_k = (t_k - y_k) \cdot f'(y_{-}in_k)$$

$$\Delta w_{jk} = \alpha \cdot \delta_k \cdot z_j$$

$$1$$

$$X_1 \cdot \cdot \cdot \cdot X_k$$

$$X_1 \cdot \cdot \cdot \cdot \cdot X_k$$

$$\frac{\partial E}{\partial y} = (y - t)$$

$$\frac{\partial y}{\partial y_{in}} = -1 \cdot \left(1 + e^{-\lambda \cdot y_{-}in}\right)^{-2} \cdot e^{-\lambda \cdot y_{-}in} \cdot (-\lambda)$$

$$= \lambda \cdot \frac{e^{-\lambda \cdot y_{-}in} + 1 - 1}{(1 + e^{-\lambda \cdot y_{-}in})^{2}} = \lambda \cdot \left(\frac{\left(1 + e^{-\lambda \cdot y_{-}in}\right)}{(1 + e^{-\lambda \cdot y_{-}in})^{2}} - \frac{1}{(1 + e^{-\lambda \cdot y_{-}in})^{2}}\right)$$

$$= \lambda \cdot (y - y^{2}) = \lambda \cdot y \cdot (1 - y)$$

$$\Delta w_i = -\alpha \cdot (\nu - t) \cdot \lambda \cdot \nu \cdot (1 - \nu) \cdot x_i$$

$$\Delta w_{jk} = \alpha \cdot (t_k - y_k) \cdot \lambda \cdot y \cdot (1 - y) \cdot z_j$$

$$\delta_{-}in_{j} = \sum_{k=1}^{m} \delta_{k} \cdot w_{jk}$$

$$\delta_{j} = \delta_{-}in_{j} \cdot f'\left(z_{in_{j}}\right)$$

$$\Delta v_{ij} = \alpha \cdot \delta_{j} \cdot x_{i}$$

$$\frac{\partial W_{i}}{\partial y} = \frac{\partial W_{i}}{\partial y} \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial E}{\partial y} \cdot \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial W_{i}}{\partial y} = \sum_{i=1}^{m} \frac{\partial W_{i}}{\partial y$$

$$\frac{\partial y}{\partial y} = \sum_{i=1}^{m} \frac{\partial y_{i}n_{i}}{\partial y_{i}}$$

 $\partial E$ 

 $\Delta w_i = -\alpha \cdot \left( \sum_{i=1}^{m} (y_i - t_i) \cdot \lambda \cdot y_i \cdot (1 - y_i) \cdot w_i \right) \lambda \cdot z \cdot (1 - z) \cdot x_i$ 

 $\Delta v_{ij} = \alpha \cdot \left( \sum_{k=1}^{m} (t_k - y_k) \cdot \lambda \cdot y_k \cdot (1 - y_k) \cdot w_{kj} \right) \lambda \cdot z_j \cdot (1 - z_j) \cdot x_i$ 

$$(1 \cdot \lambda \cdot y_i \cdot (1 \cdot y_i))$$

$$\frac{\partial y}{\partial v \ in} = \lambda \cdot z \cdot (1 - z) \qquad \frac{\partial y_{-in}}{\partial w_{i}} = x_{i}$$

$$\sum_{i=1}^{N} (y_i - t_i) \cdot \lambda \cdot y_i \cdot (1 - t_i)$$

$$= \sum_{i=1}^{m} (y_i - t_i) \cdot \lambda \cdot y_i \cdot (1 - y_i) \cdot w_i$$

 $\partial E$   $\partial y$   $\partial y_i$ in

 $\frac{\partial w_i}{\partial w_i} = \frac{\partial w_i}{\partial y_i} \cdot \frac{\partial w_i}{\partial w_i}$ 

$$= \sum_{i=1}^{\infty} \frac{\partial y}{\partial y} \cdot \frac{\partial y_{i} \cdot n_{i}}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i} \cdot n_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} \cdot \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y_{i}} = \sum_{i=1}^{\infty} \frac{\partial y}{\partial y$$

$$Z_j$$
  $\delta_j$