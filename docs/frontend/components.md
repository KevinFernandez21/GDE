# Componentes Frontend GDE

## 🧩 Arquitectura de Componentes

### Estructura de Carpetas
```
components/
├── ui/                   # Componentes base (Shadcn/ui)
│   ├── button.tsx
│   ├── input.tsx
│   ├── table.tsx
│   ├── dialog.tsx
│   ├── form.tsx
│   └── ...
├── forms/               # Formularios específicos
│   ├── ProductForm.tsx
│   ├── GuiaForm.tsx
│   ├── CostoForm.tsx
│   └── ...
├── tables/              # Tablas con TanStack Table
│   ├── ProductsTable.tsx
│   ├── GuiasTable.tsx
│   ├── KardexTable.tsx
│   └── ...
├── charts/              # Gráficos con Recharts
│   ├── StockChart.tsx
│   ├── SalesChart.tsx
│   ├── CostChart.tsx
│   └── ...
├── layout/              # Componentes de layout
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── Navigation.tsx
│   └── ...
├── features/            # Componentes por funcionalidad
│   ├── inventory/
│   ├── guias/
│   ├── pistoleo/
│   ├── contabilidad/
│   └── ...
└── common/              # Componentes comunes
    ├── LoadingSpinner.tsx
    ├── ErrorBoundary.tsx
    ├── ConfirmDialog.tsx
    └── ...
```

## 🎨 Componentes UI Base

### Button Component
```typescript
// components/ui/button.tsx
interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  loading?: boolean
}
```

### Input Component
```typescript
// components/ui/input.tsx
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url'
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  error?: string
  disabled?: boolean
  required?: boolean
}
```

### Table Component
```typescript
// components/ui/table.tsx
interface TableProps<T> {
  data: T[]
  columns: ColumnDef<T>[]
  onRowClick?: (row: T) => void
  pagination?: boolean
  sorting?: boolean
  filtering?: boolean
}
```

## 📝 Formularios

### ProductForm
```typescript
// components/forms/ProductForm.tsx
interface ProductFormProps {
  product?: Product
  onSubmit: (data: ProductFormData) => void
  onCancel: () => void
  isLoading?: boolean
}

const ProductForm: React.FC<ProductFormProps> = ({
  product,
  onSubmit,
  onCancel,
  isLoading
}) => {
  const form = useForm<ProductFormData>({
    resolver: zodResolver(productSchema),
    defaultValues: product || {}
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Campos del formulario */}
      </form>
    </Form>
  )
}
```

### GuiaForm
```typescript
// components/forms/GuiaForm.tsx
interface GuiaFormProps {
  guia?: Guia
  onSubmit: (data: GuiaFormData) => void
  onCancel: () => void
  isLoading?: boolean
}

const GuiaForm: React.FC<GuiaFormProps> = ({
  guia,
  onSubmit,
  onCancel,
  isLoading
}) => {
  // Implementación del formulario de guías
}
```

### CostoForm
```typescript
// components/forms/CostoForm.tsx
interface CostoFormProps {
  costo?: Costo
  onSubmit: (data: CostoFormData) => void
  onCancel: () => void
  isLoading?: boolean
}

const CostoForm: React.FC<CostoFormProps> = ({
  costo,
  onSubmit,
  onCancel,
  isLoading
}) => {
  // Implementación del formulario de costos
}
```

## 📊 Tablas

### ProductsTable
```typescript
// components/tables/ProductsTable.tsx
interface ProductsTableProps {
  products: Product[]
  onEdit: (product: Product) => void
  onDelete: (product: Product) => void
  onViewKardex: (product: Product) => void
  isLoading?: boolean
}

const ProductsTable: React.FC<ProductsTableProps> = ({
  products,
  onEdit,
  onDelete,
  onViewKardex,
  isLoading
}) => {
  const columns: ColumnDef<Product>[] = [
    {
      accessorKey: 'code',
      header: 'Código',
      cell: ({ row }) => (
        <div className="font-mono">{row.getValue('code')}</div>
      )
    },
    {
      accessorKey: 'name',
      header: 'Nombre',
      cell: ({ row }) => (
        <div className="font-medium">{row.getValue('name')}</div>
      )
    },
    {
      accessorKey: 'stock_actual',
      header: 'Stock',
      cell: ({ row }) => {
        const stock = row.getValue('stock_actual') as number
        const stockMinimo = row.original.stock_minimo
        return (
          <div className={cn(
            "font-medium",
            stock <= stockMinimo ? "text-red-600" : "text-green-600"
          )}>
            {stock}
          </div>
        )
      }
    },
    {
      id: 'actions',
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => onEdit(row.original)}>
              Editar
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => onViewKardex(row.original)}>
              Ver Kardex
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem 
              onClick={() => onDelete(row.original)}
              className="text-red-600"
            >
              Eliminar
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    }
  ]

  return (
    <DataTable
      columns={columns}
      data={products}
      isLoading={isLoading}
    />
  )
}
```

### GuiasTable
```typescript
// components/tables/GuiasTable.tsx
interface GuiasTableProps {
  guias: Guia[]
  onEdit: (guia: Guia) => void
  onView: (guia: Guia) => void
  onUpdateStatus: (guia: Guia, status: GuiaStatus) => void
  isLoading?: boolean
}

const GuiasTable: React.FC<GuiasTableProps> = ({
  guias,
  onEdit,
  onView,
  onUpdateStatus,
  isLoading
}) => {
  const columns: ColumnDef<Guia>[] = [
    {
      accessorKey: 'codigo',
      header: 'Código',
      cell: ({ row }) => (
        <div className="font-mono">{row.getValue('codigo')}</div>
      )
    },
    {
      accessorKey: 'cliente_nombre',
      header: 'Cliente',
      cell: ({ row }) => (
        <div className="font-medium">{row.getValue('cliente_nombre')}</div>
      )
    },
    {
      accessorKey: 'estado',
      header: 'Estado',
      cell: ({ row }) => {
        const estado = row.getValue('estado') as string
        return (
          <Badge variant={getEstadoVariant(estado)}>
            {estado}
          </Badge>
        )
      }
    },
    {
      accessorKey: 'fecha_creacion',
      header: 'Fecha',
      cell: ({ row }) => {
        const fecha = row.getValue('fecha_creacion') as string
        return (
          <div className="text-sm text-muted-foreground">
            {format(new Date(fecha), 'dd/MM/yyyy')}
          </div>
        )
      }
    }
  ]

  return (
    <DataTable
      columns={columns}
      data={guias}
      isLoading={isLoading}
    />
  )
}
```

## 📈 Gráficos

### StockChart
```typescript
// components/charts/StockChart.tsx
interface StockChartProps {
  data: StockData[]
  title?: string
  height?: number
}

const StockChart: React.FC<StockChartProps> = ({
  data,
  title = "Stock por Categoría",
  height = 300
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="categoria" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="stock" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
```

### SalesChart
```typescript
// components/charts/SalesChart.tsx
interface SalesChartProps {
  data: SalesData[]
  title?: string
  height?: number
}

const SalesChart: React.FC<SalesChartProps> = ({
  data,
  title = "Ventas por Mes",
  height = 300
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={height}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="ventas" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
```

## 🏗️ Layout Components

### Header
```typescript
// components/layout/Header.tsx
interface HeaderProps {
  user: User
  onLogout: () => void
}

const Header: React.FC<HeaderProps> = ({ user, onLogout }) => {
  return (
    <header className="border-b">
      <div className="flex h-16 items-center px-4">
        <div className="flex items-center space-x-4">
          <Logo />
          <Navigation />
        </div>
        <div className="ml-auto flex items-center space-x-4">
          <UserMenu user={user} onLogout={onLogout} />
        </div>
      </div>
    </header>
  )
}
```

### Sidebar
```typescript
// components/layout/Sidebar.tsx
interface SidebarProps {
  user: User
  currentPath: string
}

const Sidebar: React.FC<SidebarProps> = ({ user, currentPath }) => {
  const navigation = getNavigationItems(user.role)

  return (
    <aside className="w-64 border-r">
      <nav className="p-4">
        {navigation.map((item) => (
          <NavItem
            key={item.href}
            item={item}
            isActive={currentPath === item.href}
          />
        ))}
      </nav>
    </aside>
  )
}
```

## 🔫 Componentes de Pistoleo

### ScannerComponent
```typescript
// components/features/pistoleo/ScannerComponent.tsx
interface ScannerComponentProps {
  onScan: (code: string) => void
  onError: (error: string) => void
  isActive: boolean
}

const ScannerComponent: React.FC<ScannerComponentProps> = ({
  onScan,
  onError,
  isActive
}) => {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!isActive) return

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      } catch (error) {
        onError('Error al acceder a la cámara')
      }
    }

    startCamera()
  }, [isActive, onError])

  return (
    <div className="relative">
      <video
        ref={videoRef}
        className="w-full h-64 object-cover rounded-lg"
        autoPlay
        playsInline
      />
      <canvas
        ref={canvasRef}
        className="hidden"
      />
    </div>
  )
}
```

### PistoleoSession
```typescript
// components/features/pistoleo/PistoleoSession.tsx
interface PistoleoSessionProps {
  session: PistoleoSession
  onEndSession: () => void
  onScan: (code: string) => void
}

const PistoleoSession: React.FC<PistoleoSessionProps> = ({
  session,
  onEndSession,
  onScan
}) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Sesión de Pistoleo</CardTitle>
        <CardDescription>
          {session.nombre_sesion} - {session.escaneos_totales} escaneos
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ScannerComponent
          onScan={onScan}
          onError={(error) => toast.error(error)}
          isActive={true}
        />
        <div className="mt-4 flex justify-end">
          <Button onClick={onEndSession} variant="destructive">
            Finalizar Sesión
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
```

## 🔧 Componentes Comunes

### LoadingSpinner
```typescript
// components/common/LoadingSpinner.tsx
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  text?: string
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  text
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  }

  return (
    <div className="flex flex-col items-center justify-center space-y-2">
      <Loader2 className={cn("animate-spin", sizeClasses[size])} />
      {text && <p className="text-sm text-muted-foreground">{text}</p>}
    </div>
  )
}
```

### ErrorBoundary
```typescript
// components/common/ErrorBoundary.tsx
interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<{ error: Error }>
}

class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  { hasError: boolean; error?: Error }
> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback
      return <FallbackComponent error={this.state.error!} />
    }

    return this.props.children
  }
}
```

### ConfirmDialog
```typescript
// components/common/ConfirmDialog.tsx
interface ConfirmDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description: string
  onConfirm: () => void
  onCancel: () => void
  confirmText?: string
  cancelText?: string
  variant?: 'default' | 'destructive'
}

const ConfirmDialog: React.FC<ConfirmDialogProps> = ({
  open,
  onOpenChange,
  title,
  description,
  onConfirm,
  onCancel,
  confirmText = 'Confirmar',
  cancelText = 'Cancelar',
  variant = 'default'
}) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>
            {cancelText}
          </Button>
          <Button
            variant={variant}
            onClick={onConfirm}
          >
            {confirmText}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

## 🎯 Patrones de Componentes

### 1. Compound Components
```typescript
// Ejemplo: Card con header y content
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
  </CardHeader>
  <CardContent>
    Contenido
  </CardContent>
</Card>
```

### 2. Render Props
```typescript
// Ejemplo: DataTable con render personalizado
<DataTable
  data={products}
  renderActions={(row) => (
    <DropdownMenu>
      <DropdownMenuItem onClick={() => onEdit(row)}>
        Editar
      </DropdownMenuItem>
    </DropdownMenu>
  )}
/>
```

### 3. Custom Hooks
```typescript
// Ejemplo: useProducts hook
const { products, isLoading, error, createProduct, updateProduct } = useProducts()
```

## 📱 Responsive Design

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Componentes Adaptativos
```typescript
// Ejemplo: Tabla responsiva
const ResponsiveTable = ({ data, columns }) => {
  const isMobile = useMediaQuery('(max-width: 768px)')
  
  if (isMobile) {
    return <MobileTable data={data} />
  }
  
  return <DesktopTable data={data} columns={columns} />
}
```

## 🧪 Testing de Componentes

### Unit Tests
```typescript
// __tests__/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../Button'

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    fireEvent.click(screen.getByText('Click me'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### Integration Tests
```typescript
// __tests__/components/ProductForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { ProductForm } from '../ProductForm'

describe('ProductForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = jest.fn()
    render(<ProductForm onSubmit={onSubmit} onCancel={jest.fn()} />)
    
    fireEvent.change(screen.getByLabelText('Código'), {
      target: { value: 'PROD001' }
    })
    fireEvent.change(screen.getByLabelText('Nombre'), {
      target: { value: 'Producto Test' }
    })
    
    fireEvent.click(screen.getByText('Guardar'))
    
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        code: 'PROD001',
        name: 'Producto Test'
      })
    })
  })
})
```





