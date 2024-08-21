
import { HTMLInputTypeAttribute } from "react";
import { Control, Controller, FieldValues, Path } from "react-hook-form";
import { FormControl, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";


interface LabeledInputProps<T extends FieldValues> {
    className?: string;
    name: Path<T>;
    control: Control<T>;
    placeholder?: string;
    label: string;
    type?: HTMLInputTypeAttribute | undefined;

}

export const LabeledFormInput: React.FC<LabeledInputProps> = ({
    className,
    name,
    control,
    placeholder,
    label,
    type,

}) => {
    return (
        <div className={`flex-1 space-y-4 ${className ? className : ''}`}>
            <Controller
                name={name}
                control={control}
                render={({ field, fieldState: { error } }) => (
                    <FormItem className="mb-1 space-y-1">
                        <FormControl>
                            <>
                                <FormLabel>{label}</FormLabel>
                                <Input type={type} placeholder={placeholder} {...field} /></>

                        </FormControl>
                        {error && <FormMessage className="text-[10px]">{error.message}</FormMessage>}
                    </FormItem>
                )}
            />
        </div>
    );
};