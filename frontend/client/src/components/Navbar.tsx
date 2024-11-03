"use client";

import Link from "next/link";
import { useAuth } from "../context/AuthContext";
import UserDataModal from "./UserDataModal";
import Image from "next/image";
import { useRouter } from "next/navigation";

export default function Navbar() {
    const { token, logout } = useAuth();
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push("/login");
    };

    return (
        <nav className="max-w-6xl m-auto bg-background text-foreground p-4 font-jetbrains">
            <div className="container mx-auto flex justify-between">
                <Link href="/" className="text-primary font-bold">
                    <Image
                        src="https://quarkinvestimentos.com.br/wp-content/uploads/2022/09/investimentos-sp-6.png"
                        alt="Quark Logo"
                        width={180}
                        height={38}
                        priority
                    />
                </Link>
                <div className="flex items-center space-x-4">
                    {token ? (
                        <>
                            <Link href="/clients" className="text-secondary hover:text-primary">
                                Clients
                            </Link>
                            <Link href="/operations" className="text-secondary hover:text-primary">
                                Operations
                            </Link>
                            <Link href="/register" className="text-secondary hover:text-primary">
                                Register User
                            </Link>
                            <UserDataModal />
                            <button
                                onClick={handleLogout}
                                className="text-secondary hover:text-primary"
                            >
                                Logout
                            </button>
                        </>
                    ) : (
                        <Link href="/login" className="text-secondary hover:text-primary">
                            Login
                        </Link>
                    )}
                </div>
            </div>
        </nav>
    );
}