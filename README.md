# SFU CMPT 756 GanFanCrew Term Project Directory

This is our term project for CMPT 756 (Spring 2022)


## Instantiate the template files

#### Fill in the required values in the template variable file

Copy the file `cluster/tpl-vars-blank.txt` to `cluster/tpl-vars.txt`
and fill in all the required values in `tpl-vars.txt`.  These include
things like your AWS keys, your GitHub signon, and other identifying
information.  See the comments in that file for details. Note that you
will need to have installed Gatling
(https://gatling.io/open-source/start-testing/) first, because you
will be entering its path in `tpl-vars.txt`.

#### Instantiate the templates

Once you have filled in all the details, run

~~~
$ make -f k8s-tpl.mak templates
~~~

This will check that all the programs you will need have been
installed and are in the search path.  If any program is missing,
install it before proceeding.

The script will then generate makefiles personalized to the data that
you entered in `clusters/tpl-vars.txt`.

**Note:** This is the *only* time you will call `k8s-tpl.mak`
directly. This creates all the non-templated files, such as
`k8s.mak`.  You will use the non-templated makefiles in all the
remaining steps.


## Create Kubernetes cluster on AWS EKS

#### 1. Run container
~~~
tools/shell.sh
~~~

#### 2. Check tables in AWS DynamoDB
~~~
aws dynamodb list-tables
~~~
If the db stack exists, but the resulting output not include tables `User`, `Music` and `Playlist`, delete the stack first:
~~~
aws cloudformation delete-stack --stack-name db-ZZ-REG-ID
~~~

#### 3. Start empty Kubernetes cluster
~~~
make -f eks.mak start
~~~
It will use Amazon EC2 t3.large instance with 5 work nodes.

#### 4. Deploy all services
~~~
make -f k8s.mak provision
~~~
There will be 5 replicas for three public micro-services respectively, 10 replicas for DB service, and 500 read and write units for DynamoDB.

#### 5. Check tables in AWS DynamoDB
~~~
aws dynamodb list-tables
~~~
The resulting output should include tables `User`, `Music` and `Playlist`.


## Use Playlist client 
The `Pcli` is a client for `Playlist` service.

#### 1. Get external IP to access to the cluster
~~~
kubectl -n istio-system get service istio-ingressgateway | cut -c -140
~~~

#### 2. Run Pcli
~~~
cd pcli
~~~
~~~
make PORT=80 SERVER=EXTERNAL-IP build-pcli
~~~
~~~
make PORT=80 SERVER=EXTERNAL-IP run-pcli
~~~

## Monitor pods
~~~
k9s
~~~

## Use Grafana
#### 1. Get the Grafana URL
~~~
make -f k8s.mak grafana-url
~~~
Copy this URL and paste it into the browser. It will show the Grafana signon page.

#### 2. Sign on to Grafana dashboard
* User: admin
* Password: prom-operator

Select “Browse” from the menu. This will bring up a list of dashboards. Click on c756 transactions

## View Kiali graph
#### 1. Get the the Kiali URL
~~~
make -f k8s.mak kiali-url
~~~
Copy this URL and paste it into the browser

#### 2. Set Kiali graph
* Namespaces: c756ns
* Graph type: Versioned app graph
* Display interval: Last 1m
* Refresh interval: Every 30s
* Display:
    * Show Edge Labels: Traffic Rate
    * Show: Compressed Hide, Operation Nodes, Service Nodes, Traffic Animation
    * Show Badges: Virtual Services

## Start simulation
(Make sure to start a new terminal window and you're not in tools/shell.sh)
Send initial loads to the system
~~~
./gatling-1-user.sh
./gatling-10-music.sh
./gatling-10-playlist.sh
./gatling-10-user.sh
~~~
Send medium loads to the system
~~~
./gatling-100-music.sh
./gatling-100-playlist.sh
./gatling-100-user.sh
~~~
Send heavy loads to the system 
~~~
./gatling-260-music.sh
./gatling-260-playlist.sh
./gatling-260-user.sh
~~~

#### Stop gatling
If want to delete all the Gatling jobs
~~~
tools/kill-gatling.sh
~~~

## Close cluster
~~~
make -f eks.mak stop
~~~

### Simple Repo Structure

This is the tree of this repo. 
```
├── ./.github	
│   └── ./.github/workflows     # Github CI action
├── ./ci                        # CI test
│   ├── ./ci/playlist           # new test for Playlist
│   ├── ./ci/v1
│   └── ./ci/v1.1
├── ./cluster                   # cluster configuration files 
├── ./db                        # database micro-service
├── ./gatling			        
│   ├── ./gatling/resources     # data for three public micro-services
│   └── ./gatling/simulation    # simulations scenarios
├── ./loader                    # utility to load DynamoDB tables
├── ./mcli                      # client for Music service
├── ./pcli                      # client for Playlist service
├── ./reference                 # reference material for istio and Prometheus
├── ./s1                        # user micro-service
├── ./s2				        
├── ./s2                        # music micro-service
│   ├── ./s2/v1
│   ├── ./s2/v1.1
│   └── ./s2/v2
├── ./s3                        # playlist micro-service
│   └── ./s3/v1
├── ./tools                     # assorted shell scripts
├── ./eks-tpl.mak               # makefile for Amazon EKS cluster
├── ./gatling-*.sh              # shell script for create Gatling jobs
├── ./k8s-tpl.mak               # makefile working with Kubernetes cluster
├── ./obs.mak                   # sub-make file
└── ./README.md                 # README file for project
```