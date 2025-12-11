
# VPN

```
cd ansible
ansible-playbook -i inventory.ini playbook.yml --vault-password-file password.txt
```

or 

```
eval $(minikube docker-env)

docker build -t app-image:latest ./app
docker build -t vpn-image:latest ./vpn

kubectl apply k k8s/
```

Then

```
kubectl port-forward svc/nginx 30030:80 -n app
kubectl port-forward svc/grafana 30060:3000 -n monitoring
kubectl port-forward svc/kibana 30090:5601 -n logging
```

Go to

```
localhost:30030 -> application
localhost:30060 -> grafana
localhost:30090 -> kibana
```

-  for hpa checking, start very large load from the browser and you can see pods increasing

## for EFk viz

### Step 1: Tell Kibana where the data is

Before you can see anything, you must define an **Index Pattern**. This tells Kibana: *"Look at all indices starting with `filebeat-`"*.

1.  Open **[http://localhost:5601](https://www.google.com/search?q=http://localhost:5601)** in your browser.
2.  Click the **Menu icon** (three horizontal lines) in the top-left corner.
3.  Scroll down to the bottom and click **Stack Management**.
4.  On the left sidebar, click **Index Patterns** (sometimes called **Data Views**).
5.  Click the blue button **Create index pattern**.
6.  In the **Name** field, type: `filebeat-*`
      * *You should see a success message saying it matches 1 source.*
7.  Click **Next step**.
8.  In the **Time field** dropdown, select **`@timestamp`**.
9.  Click **Create index pattern**.

### Step 2: See the Raw Logs (The "Discover" Tab)

Now that Kibana knows about the data, let's look at the logs coming from your VPN and App containers.

1.  Click the **Menu icon** (top-left) again.
2.  Click **Discover** (it looks like a compass).
3.  You will see a bar graph and a list of logs.
5.  **Filter for your app:**

    In the search bar, type this exactly:

      ```text
      log.file.path : *vpn*
      ```
    This shows only the VPN container logs.

    To see the App logs, change it to:

      ```text
      log.file.path : *app*
      ```

    To see Nginx logs:

      ```text
      log.file.path : *nginx*
      ```



and test

traffic goes 

```
local -> nginx rev proxy -> vpn -> app
```
Note: if minikube cant handle the efk stack, then `minikube start --memory 6144 --cpus 4 ` manally assigns enough memory and cpu to the minkube cluster.


Also make sure to increase the vm.max_map_count(shown below) as elasticsearch8 may not work without this. 
```
minikube ssh
sudo sysctl -w vm.max_map_count=262144
exit
```
