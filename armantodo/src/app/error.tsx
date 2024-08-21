'use client'
import {CiWarning} from "react-icons/ci";

export default function CustomError() {

    return (
        <div className={"flex items-center justify-center h-[60vh]"}>
            <div className={"text-center flex items-center flex-col"}>
                <CiWarning size={"48"} className={"text-destructive"}/>
                <h2 className={"text-xl"}>Something went wrongs!</h2>
                <h5 className={"text-sm"}>Please try again later.</h5>
            </div>

        </div>
    )
}