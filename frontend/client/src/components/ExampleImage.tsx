"use client";

import Image from 'next/image';

export default function ExampleImage() {
    return (
        <div>
            <h2>Our Investment Image</h2>
            <Image
                src="https://quarkinvestimentos.com.br/wp-content/uploads/2022/09/investimentos-sp-6.png"
                alt="Investimentos SP"
                width={500}
                height={300}
                className="rounded shadow-lg"
            />
        </div>
    );
} 