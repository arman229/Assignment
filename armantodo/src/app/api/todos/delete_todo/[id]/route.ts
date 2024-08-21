import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

export async function DELETE(request: Request, {params}: { params: { id: string } }) { 
 
    const id = params.id;
    if (!Number.isInteger(Number(id))) {
        return NextResponse.json({ error: 'Invalid ID' }, { status: 400 });
    }

    try {
        await prisma.todo.delete({
            where: { id: Number(id) },
        });

        return NextResponse.json({ message: 'Todo deleted successfully' }, { status: 200 });
    } catch (error: any) {
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
