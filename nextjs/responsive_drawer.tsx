'use client';
import React, { FC, ChangeEvent, useState } from 'react';
import { VscChromeClose } from 'react-icons/vsc';
import { TfiMenu } from 'react-icons/tfi';  
const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
    const [isOpen, setIsOpen] = useState(true); 

    const toggleNav = () => {
        setIsOpen(!isOpen);
    };




    return (<>
        <div className="flex  ">
            <div className={`bg-gray-300      fixed top-0 left-0 z-20 min-h-screen overflow-x-hidden transition-width duration-500 ${isOpen ? 'w-72' : 'w-0'} max-h-screen overflow-y-auto`}>
                <LeftComponent />
            </div>
            <div className={`flex-1    relative transition-all duration-300 ease-in-out ${isOpen ? 'ml-72' : 'ml-0'}`}>
                <main className="flex ">
                    <div className={`cursor-pointer  `} onClick={() => toggleNav()}>
                        {isOpen ? (<VscChromeClose />) : <TfiMenu />}
                    </div>
                    <RightComponent />
                </main>
            </div>
        </div></>
    );
};

const LeftComponent = () => {
    return (
        <div className='flex flex-col   '>
            <p>one</p>
            <p>two</p>
            <p>three</p>
            <p>four</p>
            <p>six</p>
            <p>seven</p>
        </div>
    )
}
const RightComponent = () => {
    return (
        <div className='flex flex-col'>
            <p>This is first  line</p>
            <p>This is second  line</p>
            <p>This is third   line</p>
            <p>This is  fourth line</p>
            <p>This is  fifth line</p>
            <p>This is  sixth line</p>
        </div>
    )
}

export default DashboardLayout;



