helm uninstall kafka-broker -n dev
helm uninstall delta-storage -n dev
helm uninstall strimzi-operator -n dev
helm uninstall spark-operator -n dev

kubectl delete namespace dev