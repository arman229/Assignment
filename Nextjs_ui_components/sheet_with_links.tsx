'use client'
import React, { useState } from "react";
import { Sheet, SheetContent, SheetTrigger, SheetClose } from "@/components/ui/sheet";

export const menuItems = [
    { name: 'Home', href: 'home' },
    { name: 'About', href: 'about' },
    { name: 'pricing', href: 'pricing' },
    { name: 'contactus', href: 'contactus' },
    { name: 'faq', href: 'faq' },
    { name: 'features', href: 'features' },

];


export default function MyApp() {
    const [sheetOpen, setSheetOpen] = useState(false);

    return (
        <Sheet open={sheetOpen} onOpenChange={setSheetOpen}>
            <SheetTrigger>Open</SheetTrigger>
            <SheetContent side={"left"} className="p-0">

                <nav className="flex flex-col">
                    {menuItems.map((item, index) => (
                        <Link className={`group ml-2 flex  h-9 w-max items-center justify-center  `}
                            key={index}
                            href={item.href}
                            onClick={() => setSheetOpen(false)}
                        >
                            {item.name}
                        </Link>
                    ))}
                </nav>
            </SheetContent>
        </Sheet>
    );
}




const Link = (props: any) => <a {...props} />;
