# Kubernetes Web Service with Monitoring

Проект представляет собой развёртывание веб-сервиса в Kubernetes-кластере с настройкой мониторинга через Prometheus и визуализацией метрик в Grafana.

## 🛠 Технологический стек
- **Kubernetes**: Оркестрация контейнеризированных приложений ([Официальная документация](https://kubernetes.io/ru/docs/home/))
- **Minikube**: Локальный Kubernetes-кластер ([Установка](https://minikube.sigs.k8s.io/docs/start/))
- **Docker**: Сборка и управление контейнерами ([Установка](https://docs.docker.com/get-docker/))
- **Helm**: Менеджер пакетов для Kubernetes ([Установка](https://helm.sh/docs/intro/install/))
- **Prometheus**: Система мониторинга ([Helm-чарт](https://github.com/prometheus-community/helm-charts))
- **Grafana**: Платформа для визуализации данных ([Helm-чарт](https://github.com/grafana/helm-charts))

## 📁 Структура проекта

```
.
├── app/                      # Исходный код веб-сервиса
│   ├── app.py                # Flask-приложение
│   └── requirements.txt      # Зависимости Python
├── kubernetes/               # Конфигурации Kubernetes
│   ├── deployment.yaml       # Деплоймент приложения
│   ├── service.yaml          # Сервис для доступа к подам
│   └── ingress.yaml          # Ingress для внешнего доступа
└── monitoring/               # Конфигурации мониторинга
    ├── prometheus-values.yaml# Настройки Prometheus
    └── grafana-ingress.yaml  # Ingress для Grafana
```

## 🚀 Запуск проекта

### 1. Установите зависимости

- Убедитесь, что установлены [Docker](https://docs.docker.com/get-docker/), [Minikube](https://minikube.sigs.k8s.io/docs/start/) и [Helm](https://helm.sh/docs/intro/install/).

### 2. Запустите Minikube

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### 3. Соберите Docker-образ приложения

```bash
docker build -t hello-service:latest
minikube image load hello-service:latest
```

Либо внутри кластера:

```bash
eval $(minikube docker-env)
docker build -t hello-service:latest ./app
eval $(minikube docker-env -u)
```

### 4. Разверните веб-сервис

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### 5. Настройка Prometheus и Grafana
```
bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

#### Установите Prometheus

```bash
helm install prometheus prometheus-community/prometheus \
  --set server.service.type=ClusterIP \
  --set server.persistentVolume.enabled=false
```

#### Установите Grafana
```bash
helm install grafana grafana/grafana \
  --set service.enabled=true \
  --set service.type=ClusterIP
```

### 6. Настройте доступ
```bash
echo "$(minikube ip) hello.local grafana.local" | sudo tee -a /etc/hosts
```

### 7. Проверьте работу
- Веб-сервис: http://hello.local/<name>
- Grafana: http://grafana.local (логин: admin, пароль: ```kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode```)
- Prometheus: ```kubectl port-forward svc/prometheus-server 9090:80```

## 💡 Примечания
1. Для доступа к Grafana через браузер может потребоваться портфорвардинг:

```bash
kubectl port-forward svc/grafana 3000:80
```

Затем откройте http://localhost:3000.

2. Чтобы обновить образ приложения после изменений:

```bash
kubectl rollout restart deployment hello-deployment
```

## ⚠️ Возможные ошибки и решения
### Ошибка 503 (Service Unavailable)
- Причина: Проблемы с Ingress или недоступность сервиса.

- Решение:

```bash
kubectl get pods -n ingress-nginx # Проверьте статус Ingress-контроллера
kubectl describe ingress hello-ingress # Ищите ошибки в событиях
```

### ImagePullBackOff
- Причина: Образ недоступен в Minikube.

- Решение:

```bash
eval $(minikube docker-env)
docker build -t hello-service:latest ./app
```

### CrashLoopBackOff
- Причина: Ошибка в коде приложения.

- Решение:

```bash
kubectl logs <pod-name> # Найдите ошибку в логах
```

## 📄 Лицензия
MIT License. Подробнее см. в файле LICENSE.

Чтобы использовать:
1. Скопируйте весь текст выше.
2. Сохраните в файл `README.md` в корне вашего репозитория.
3. Замените `LICENSE` на актуальную лицензию вашего проекта.
