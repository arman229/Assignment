'use client'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { useParams } from 'next/navigation'
import { toastSuccess, toastError } from '@/lib/utils'
import { useState } from 'react'
import {Card,CardContent,CardHeader,CardTitle} from "@/components/ui/card"

const DeleteConfermation = () => {
    const router = useRouter()
    const [loading, setLoading] = useState<boolean>(false)
    const { id } = useParams()

    const DeleteApiCalling = async () => {
        setLoading(true)
        try {
            const response = await fetch(`/api/todos/delete_todo/${id}`, { method: 'DELETE' })
            if (response.ok) {
                toastSuccess('Deleted successfully')
                router.push('/todos')
            } else {
                toastError('Failed to delete')
            }
        } catch (error: any) {
            toastError(error.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <>
        <Card className="max-w-md mx-auto mt-10">
                <CardHeader>
                    <CardTitle>Add New Todo</CardTitle>
                </CardHeader>
                <CardContent>
            <p>Are you sure you want to delete?</p>
            <Button disabled={loading} onClick={DeleteApiCalling}>Delete</Button>
            <Button disabled={loading} onClick={() => router.back()}>Cancel</Button></CardContent></Card>
        </>
    )
}

export default DeleteConfermation
