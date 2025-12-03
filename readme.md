## 1
 Go to https://my.zerotier.com/, create a network and Copy the **16-character Network ID** (e.g., `8056c2e21c000001`).


## 2
  Open `edge.yaml` and paste that network id in line 42

## 3


```bash
kubectl apply -f apps.yaml -f gateway-config.yaml -f edge.yaml -f monitoring.yaml
```

wait till all the containers start

## 4

 In zerotier dashboard you will see new member, that is the continer in pod, click the check box and authorize it.

 Copy the **Managed IP** assigned to it (e.g., `10.147.20.5`). this is its ip once you connect to the vpn.

## 5

Your laptop also needs to be part of vpn to access it. Run this command in yor laptop.

```
    sudo zerotier-cli join <network-id>
```
Authorize this new memebr from the dashboard
Now you should be able to access the site. 

  * HR Portal: `http://<Managed-IP>/hr`
  * Finance Portal: `http://<Managed-IP>/finance`

## 6

Since monitoring runs inside the cluster, forward the ports to your local machine:

```bash
kubectl port-forward svc/grafana 3000:3000
```

  * **URL:** `http://localhost:3000`
  * **Login:** `admin` / `admin`
  * **Setup:** Add Data Source -\> Prometheus -\> URL: `http://prometheus:9090`

after these you can create viz taht you want from the prometheus datsource

## 7

To stop and remove everything:

```bash
kubectl delete -f apps.yaml -f gateway-config.yaml -f edge.yaml -f monitoring.yaml
```