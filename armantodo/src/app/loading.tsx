"use client";

import {RotatingLines,} from "react-loader-spinner";

export default function CustomLoading() {

    return (
        <div>

            <div className="  flex items-center justify-center h-[64vh]   ">
                <RotatingLines
                    visible={true}
                    width="64"
                    strokeColor="gray"
                    strokeWidth="1"
                    animationDuration="0.75"
                    ariaLabel="rotating-lines-loading"
                />

            </div>
        </div>
    )
}





