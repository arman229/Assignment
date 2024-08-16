'use client'
import { ChangeEvent, useState, FC } from "react";
import { Button } from "@/components/ui/button"
import { FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import Image from "next/image";
const MyPractice = () => {
    const [logoFile, setLogoFile] = useState<File | null>(null);
    const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
        // @ts-ignore
        const file = e.target.files[0];
        if (file) {
            setLogoFile(file);
        }
    };

    return (
        <>  <FormLabel>upload logo </FormLabel>
            <div className={"flex  items-center gap-2 my-2"}>

                <input
                    id="imageInput"
                    type="file"
                    name={"logo"}
                    accept="image/*"
                    onChange={handleImageChange}
                    style={{ display: 'none' }}
                />

                <CustomImage
                    className={"rounded-lg"}
                    placeholder={"/assets/images/company_image_placeholder.png"}
                    alt={"organization logo"} width={100} height={20}
                    src={logoFile == null ? undefined : URL.createObjectURL(logoFile)}
                />

                <Button onClick={() => {
                    document.getElementById('imageInput')?.click()
                }}>Upload logo</Button>
            </div>

        </>
    )
}




interface CustomImageProps {
    src: string | undefined;
    placeholder: string,
    alt: string;
    height: number;
    width: number;
    className?: string | undefined;
}

const CustomImage: FC<CustomImageProps> = ({ className, src, alt, placeholder, height, width }) => {


    return (
        <>
            {src ? (
                <Image
                    className={className}
                    height={height}
                    width={width}
                    src={src}
                    alt={alt}
                />
            )
                : (
                    <Image
                        className={className}
                        height={height}
                        width={width}
                        src={placeholder}
                        alt={"s"}
                    />
                )
            }
        </>

    );
};






export default MyPractice