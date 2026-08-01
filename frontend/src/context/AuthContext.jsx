import { createContext, useContext, useEffect, useState } from "react";
import { getToken, removeToken } from "../utils/storage";

const AuthContext = createContext();

export function AuthProvider({ children }) {

    const [token,setToken]=useState(getToken());

    const login=(jwt)=>{

        localStorage.setItem("access_token",jwt);

        setToken(jwt);

    }

    const logout=()=>{

        removeToken();

        setToken(null);

    }

    useEffect(()=>{

        setToken(getToken());

    },[]);

    return(

        <AuthContext.Provider
            value={{
                token,
                login,
                logout,
                isAuthenticated:!!token
            }}
        >
            {children}
        </AuthContext.Provider>

    )

}

export const useAuth=()=>useContext(AuthContext);