import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }) {
  const [isAuthorized, setIsAuthorized] = useState(null);

  const refreshToken = async () => {
    // pego o refresh token no local storage e coloco na variável refreshToken
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);

    // tento fazer uma requisição do tipo post na url do refresh token enviando o refresh token

    try {
      const res = await api.post("/api/token/refresh/", {
        refresh: refreshToken,
      });
      //   se a resposta é OK então pego a resposta e coloco no Acess token, e depois seto a autirzação para Ture
      if (res.status == 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        setIsAuthorized(true);
        // se não der certo eu seto para false
      } else {
        setIsAuthorized(false);
      }
      // pego o erro e mostro no log e seto para False
    } catch (error) {
      console.log(error);
      setIsAuthorized(false);
    }
  };

  //   aqui crio a função auth responsável por pegar o token, caso não exista seto para false a autorização

  useEffect(() => {
    async function auth() {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (!token) {
        setIsAuthorized(false);
        return;
      }
      // se tiver token eu decodifico o token e pego o valor de expiracao do token, verifico se ele é menor do que a data de hoje em segundos. se for ele for eu executo o refresh token para pegar novamente o token se ainda estiver no tempo de expiração ele está autorizado ainda
      const decoded = jwtDecode(token);
      const tokenExpiration = decoded.exp;
      const now = Date.now() / 1000;

      if (tokenExpiration < now) {
        await refreshToken();
      } else {
        setIsAuthorized(true);
      }
    }
    auth().catch(() => setIsAuthorized(false));
  }, []);

  //  Caso a variável isAuthorized é null vai ficar aparecendo loading
  // se for autorizado vai retornar o children (componente ou página) se não retorna para login

  if (isAuthorized === null) {
    return <div>Loading ...</div>;
  }

  return isAuthorized ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
