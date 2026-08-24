FROM node:20-alpine

WORKDIR /app

# Сначала копируем только файлы зависимостей для кеширования слоя
COPY package*.json ./

RUN npm install

# Копируем остальной код
COPY . .

EXPOSE 5173

# Запускаем Vite с флагом --host, чтобы сервер был доступен снаружи контейнера
CMD ["npm", "run", "dev", "--", "--host"]